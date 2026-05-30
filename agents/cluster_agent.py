import sqlite3
import logging
import os
import matplotlib.pyplot as plt
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from mesa import Agent

class AgentCluster(Agent):
    """
    AgentCluster uses unsupervised learning (K-Means) to group similar opportunities.
    
    === What Clustering Achieves in this System ===
    While classification (AgentClassifier) categorizes opportunities into broad, 
    predefined buckets (e.g., 'internship', 'scholarship') using labeled data, 
    clustering groups them based on the actual nuanced text of their descriptions 
    without any human labels.
    
    For example, within the broad bucket of 'internships', clustering might automatically 
    discover a sub-group of 'Front-End React Web Dev' internships, and another sub-group 
    of 'Machine Learning Python' internships. 
    
    This achieves two things:
    1. Discovery of hidden trends: It reveals the actual latent themes in the job market.
    2. Better Recommendations: Instead of recommending all internships to a user, the 
       MAS can recommend specific highly-relevant clusters that match the user's micro-skills.
    """

    def __init__(self, model):
        super().__init__(model)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get_top_keywords(self, vectorizer, cluster_center, n_words=3) -> str:
        """
        Extract the top n keywords for a cluster based on the highest TF-IDF weights 
        in the cluster center vector. This allows us to auto-generate a descriptive name.
        """
        # Get feature names (the vocabulary)
        feature_names = vectorizer.get_feature_names_out()
        
        # Sort the cluster center values and get the top n indices
        top_indices = cluster_center.argsort()[-n_words:][::-1]
        
        # Map indices to actual words and combine them
        top_words = [feature_names[i] for i in top_indices]
        return "-".join(top_words).title()

    def elbow(self, db_path: str = None):
        """
        Tests K-Means with k=2 to 10 and plots the inertia (Sum of Squared Distances)
        to visually justify the choice of k=5 via the 'Elbow Method'.
        """
        if not db_path:
            db_path = self.model.config.get("DB_PATH", "db/observatory.db")
            
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                # We cluster only classified items to ensure we have good clean data
                cursor.execute("SELECT title, description FROM Opportunities WHERE classified = 1")
                rows = cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error connecting to DB for elbow method: {e}")
            return
            
        if len(rows) < 10:
            self.logger.warning("Not enough data to run elbow method (need at least 10 items).")
            return
            
        # Combine title and description for richer text features
        texts = [f"{row[0]} {row[1]}" for row in rows]
        
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(texts)
        
        inertias = []
        K_range = range(2, 11)
        
        self.logger.info("Calculating K-Means inertia for K=2..10...")
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            
        # Plotting the Elbow Curve
        plt.figure(figsize=(8, 5))
        plt.plot(K_range, inertias, 'bx-')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Inertia (Sum of Squared Distances)')
        plt.title('Elbow Method For Optimal k')
        
        # Ensure plot directory exists
        os.makedirs("output", exist_ok=True)
        plot_path = "output/elbow_plot.png"
        plt.savefig(plot_path)
        plt.close()
        
        self.logger.info(f"Elbow plot saved successfully to {plot_path}")
        print(f"\n[AgentCluster] Generated Elbow Plot at {plot_path}.")
        print("-> Use this plot to visually justify your choice of k=5 to your professor!\n")

    def step(self):
        """
        1. Load classified opportunities.
        2. Vectorize text.
        3. Cluster with KMeans (k=5).
        4. Save to DB.
        5. Print summaries.
        """
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Load all classified opportunities
                cursor.execute("SELECT id, title, description FROM Opportunities WHERE classified = 1")
                rows = cursor.fetchall()
                
                if len(rows) < 5:
                    self.logger.warning(f"Not enough classified data to cluster (found {len(rows)}). Need at least 5.")
                    return
                    
                self.logger.info(f"Clustering {len(rows)} classified opportunities...")
                
                # Combine title and description for richer text features
                opp_ids = [row[0] for row in rows]
                texts = [f"{row[1]} {row[2]}" for row in rows]
                
                # 2. Vectorize using TF-IDF
                vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
                X = vectorizer.fit_transform(texts)
                
                # 3. Run K-Means clustering (k=5)
                k = 5
                kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
                kmeans.fit(X)
                
                cluster_labels = kmeans.labels_
                cluster_centers = kmeans.cluster_centers_
                
                # Generate dynamic names for each cluster based on top 3 keywords
                cluster_names = {}
                for i in range(k):
                    cluster_names[i] = self.get_top_keywords(vectorizer, cluster_centers[i], n_words=3)
                
                # First, clear old clusters to prevent duplicate accumulation during repeated steps
                cursor.execute("DELETE FROM OpportunityClusters")
                
                updates = []
                cluster_counts = {i: 0 for i in range(k)}
                
                for idx, opp_id in enumerate(opp_ids):
                    c_id = int(cluster_labels[idx]) # Convert numpy int32 to standard python int
                    c_name = cluster_names[c_id]
                    updates.append((c_id, c_name, opp_id))
                    cluster_counts[c_id] += 1
                    
                # 4. Save cluster assignments to OpportunityClusters
                cursor.executemany('''
                    INSERT INTO OpportunityClusters (cluster_id, cluster_name, opportunity_id)
                    VALUES (?, ?, ?)
                ''', updates)
                
                conn.commit()
                
                # Update Model Metrics for the Dashboard DataCollector
                self.model.clusters_formed = k
                
                # 5. Print cluster summaries
                print("\n=== Clustering Summary ===")
                for c_id in range(k):
                    print(f"Cluster {c_id} [{cluster_names[c_id]}]: {cluster_counts[c_id]} opportunities")
                print("==========================\n")
                
        except Exception as e:
            self.logger.error(f"Error during clustering step: {e}")
