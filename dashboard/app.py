import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

# --- Config & Setup ---
st.set_page_config(page_title="Observatory Dashboard", page_icon="🔭", layout="wide")

# Professional Theme Styling
st.markdown("""
<style>
    /* Clean, modern aesthetic */
    .reportview-container { background: #F8F9FA; }
    h1, h2, h3 { color: #2C3E50; }
    .stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# Resolve DB Path dynamically based on this file's location
DB_PATH = Path(__file__).resolve().parent.parent / "db" / "observatory.db"

# --- Data Caching ---
# Using st.cache_data prevents re-querying the database every time a UI element is clicked
@st.cache_data(ttl=60)
def load_data(query: str, params: tuple = ()) -> pd.DataFrame:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# --- Sidebar Navigation ---
st.sidebar.markdown("## 🔭 Intelligent University\n### Observatory MAS")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Overview", "Opportunities", "Clusters", "Recommendations", "Alerts / Notifications"])
st.sidebar.markdown("---")
st.sidebar.markdown(
    '''
    <div style="text-align: center; margin-bottom: 15px; padding: 10px; background-color: #2C3E50; border-radius: 10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif" width="45" style="border-radius: 50%; margin-right: 15px;"/>
        <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/25.gif" width="45"/>
        <br>
        <span style="font-size: 13px; color: #F8F9FA;"><b><i>Scanning the globe...</i></b></span>
    </div>
    ''',
    unsafe_allow_html=True
)
st.sidebar.info("🤖 MAS Background Processes Active")

# ==========================================
# 1. OVERVIEW PAGE
# ==========================================
if page == "Overview":
    st.title("📊 System Overview")
    
    # Fetch Metric Counts
    df_opps = load_data("SELECT COUNT(*) as count FROM Opportunities")
    df_users = load_data("SELECT COUNT(*) as count FROM Users")
    df_clusters = load_data("SELECT COUNT(DISTINCT cluster_id) as count FROM OpportunityClusters")
    df_notifs = load_data("SELECT COUNT(*) as count FROM Notifications WHERE status = 'pending'")
    
    # Render Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Opportunities", df_opps['count'].iloc[0] if not df_opps.empty else 0)
    col2.metric("Registered Students", df_users['count'].iloc[0] if not df_users.empty else 0)
    col3.metric("Semantic Clusters", df_clusters['count'].iloc[0] if not df_clusters.empty else 0)
    col4.metric("Pending Alerts", df_notifs['count'].iloc[0] if not df_notifs.empty else 0)
    
    st.markdown("---")
    
    # Render Plotly Bar Chart
    df_types = load_data("SELECT type, COUNT(*) as count FROM Opportunities GROUP BY type")
    if not df_types.empty:
        fig = px.bar(
            df_types, 
            x='type', y='count', 
            color='type', 
            title="Opportunities by Source Type", 
            text_auto=True,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for charts yet.")

# ==========================================
# 2. OPPORTUNITIES PAGE
# ==========================================
elif page == "Opportunities":
    st.title("💼 Browse Opportunities")
    
    # Fetch data
    df_opps = load_data("SELECT id, type, title, description, url, deadline, source, location, eligibility, category FROM Opportunities")
    
    if df_opps.empty:
        st.info("No opportunities in the database.")
    else:
        # Render Search & Filters
        col1, col2, col3 = st.columns(3)
        type_filter = col1.selectbox("Filter by Type", ["All"] + list(df_opps['type'].dropna().unique()))
        loc_filter = col2.selectbox("Filter by Location", ["All"] + list(df_opps['location'].dropna().unique()))
        search_query = col3.text_input("Search Title or Description 🔍")
        
        # Apply Filters
        filtered_df = df_opps.copy()
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
        if loc_filter != "All":
            filtered_df = filtered_df[filtered_df['location'] == loc_filter]
        if search_query:
            filtered_df = filtered_df[
                filtered_df['title'].str.contains(search_query, case=False, na=False) | 
                filtered_df['description'].str.contains(search_query, case=False, na=False)
            ]
            
        st.markdown(f"**Showing {len(filtered_df)} opportunities:**")
        
        # Format the table for display (exclude long descriptions)
        display_df = filtered_df[['id', 'title', 'type', 'category', 'location', 'deadline']].set_index('id')
        
        # Interactive Table with Selection
        event = st.dataframe(
            display_df, 
            use_container_width=True, 
            on_select="rerun", 
            selection_mode="single-row"
        )
        
        # Expand row details when clicked
        if event.selection.rows:
            selected_idx = event.selection.rows[0]
            selected_id = display_df.index[selected_idx]
            selected_row = df_opps[df_opps['id'] == selected_id].iloc[0]
            
            st.markdown("### 🔍 Opportunity Details")
            st.info(f"**{selected_row['title']}**")
            cols = st.columns(2)
            cols[0].write(f"**Type:** {selected_row['type']} | **Category:** {selected_row['category']}")
            cols[1].write(f"**Location:** {selected_row['location']} | **Deadline:** {selected_row['deadline']}")
            st.write(f"**Source:** {selected_row['source']}")
            st.write(f"**Eligibility Requirements:** {selected_row['eligibility']}")
            st.write("**Full Description:**")
            st.write(selected_row['description'])
            st.markdown(f"[🔗 View Original Posting]({selected_row['url']})")

# ==========================================
# 3. CLUSTERS PAGE
# ==========================================
elif page == "Clusters":
    st.title("🌌 Opportunity Clusters")
    st.write("Visualizing the latent semantic relationships between opportunities using TF-IDF + PCA.")
    
    df_clusters = load_data("""
        SELECT o.id, o.title, o.description, c.cluster_name 
        FROM Opportunities o
        JOIN OpportunityClusters c ON o.id = c.opportunity_id
    """)
    
    if df_clusters.empty or len(df_clusters) < 3:
        st.info("Not enough clustered data to visualize. Please run the Cluster Agent first.")
    else:
        # Perform TF-IDF + PCA on the fly for 2D visualization
        vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        texts = df_clusters['title'] + " " + df_clusters['description'].fillna('')
        X = vectorizer.fit_transform(texts)
        
        pca = PCA(n_components=2)
        coords = pca.fit_transform(X.toarray())
        
        df_clusters['pca_x'] = coords[:, 0]
        df_clusters['pca_y'] = coords[:, 1]
        
        # Render Plotly Scatter Plot
        fig = px.scatter(
            df_clusters, 
            x='pca_x', y='pca_y', 
            color='cluster_name',
            hover_name='title',
            title="PCA 2D Projection of Semantic Clusters",
            labels={'pca_x': 'Principal Component 1 (Semantic Variance)', 'pca_y': 'Principal Component 2 (Semantic Variance)'}
        )
        fig.update_layout(
            template='plotly_white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 4. RECOMMENDATIONS PAGE
# ==========================================
elif page == "Recommendations":
    st.title("🎯 Personalized Recommendations")
    
    df_users = load_data("SELECT id, name FROM Users")
    if df_users.empty:
        st.info("No users found in database.")
    else:
        # Dropdown to select a specific user
        user_dict = dict(zip(df_users['name'], df_users['id']))
        selected_user = st.selectbox("Select a Student Profile:", list(user_dict.keys()))
        
        user_id = user_dict[selected_user]
        
        # Fetch their top 10 recommendations
        df_recs = load_data('''
            SELECT o.title, o.category, r.score 
            FROM Recommendations r
            JOIN Opportunities o ON r.opportunity_id = o.id
            WHERE r.user_id = ?
            ORDER BY r.score DESC
            LIMIT 10
        ''', params=(user_id,))
        
        if df_recs.empty:
            st.warning(f"No recommendations generated yet for {selected_user}.")
        else:
            st.success(f"Top 10 AI Recommendations for {selected_user}")
            
            # Convert cosine score to a clean 0-100 percentage
            df_recs['Match %'] = (df_recs['score'] * 100).astype(int)
            
            # Show Data table with a progress bar column
            st.dataframe(
                df_recs[['title', 'category', 'Match %']], 
                use_container_width=True,
                column_config={
                    "Match %": st.column_config.ProgressColumn(
                        "Match Score Confidence",
                        help="Cosine similarity match percentage",
                        format="%d%%",
                        min_value=0,
                        max_value=100,
                    )
                }
            )
            
            # Render a horizontal bar chart of scores
            fig = px.bar(
                df_recs, 
                x='Match %', y='title', 
                color='category', 
                orientation='h',
                title=f"Confidence Scores Breakdown",
                text='Match %',
                template="plotly_white"
            )
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 5. ALERTS / NOTIFICATIONS PAGE
# ==========================================
elif page == "Alerts / Notifications":
    st.title("🔔 Alerts & Notifications")
    st.write("View the automated messages generated by the Notification Agent.")
    
    df_notifs = load_data("""
        SELECT n.id, u.name as user, o.title as opportunity, o.type, n.status, n.date_sent
        FROM Notifications n
        JOIN Users u ON n.user_id = u.id
        JOIN Opportunities o ON n.opportunity_id = o.id
        ORDER BY n.date_sent DESC
    """)
    
    if df_notifs.empty:
        st.info("No notifications have been generated yet.")
    else:
        st.success(f"Tracking {len(df_notifs)} automated alerts sent to students.")
        
        # Interactive table for alerts
        st.dataframe(
            df_notifs[['date_sent', 'user', 'opportunity', 'type', 'status']],
            use_container_width=True,
            hide_index=True
        )
