import os
import sqlite3
import subprocess
from model import ObservatoryModel

def init_db():
    print("\n[1/5] Initializing Database...")
    db_path = "db/observatory.db"
    
    # Remove existing to start fresh for demo presentation
    if os.path.exists(db_path):
        os.remove(db_path)
        
    subprocess.run(["python", "db/init_db.py"], check=True)
    print("Database initialized successfully.")

def seed_users():
    print("\n[2/5] Seeding Mock Users...")
    users = [
        ("Alice Engineering", "alice@test.edu", "Python, Machine Learning", "Data Science Internships", "Undergraduate"),
        ("Bob PhD", "bob@test.edu", "Bioinformatics, Sequence Analysis, Data", "Research, Quantum Computing", "PhD"),
        ("Charlie Postdoc", "charlie@test.edu", "Physics, String Theory", "Postdoc, Funding", "Postdoc")
    ]
    
    with sqlite3.connect("db/observatory.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO Users (name, email, skills, interests, academic_level) VALUES (?, ?, ?, ?, ?)", 
            users
        )
        conn.commit()
    print(f"Seeded {len(users)} distinct user profiles.")

def main():
    print("="*60)
    print("INTELLIGENT UNIVERSITY OBSERVATORY MAS LAUNCHER".center(60))
    print("="*60)
    
    init_db()
    seed_users()
    
    print("\n[3/5] Starting Observatory MAS Model...")
    # Initialize the model with dynamic config
    config = {
        "DB_PATH": "db/observatory.db",
        "SCRAPER_MOCK_MODE": True
    }
    model = ObservatoryModel(config)
    
    print("\n[4/5] Running Simulation Steps...")
    # Run exactly 3 steps to generate a rich dataset without looping infinitely
    for i in range(3):
        print(f"\n--- EXECUTING SIMULATION STEP {i+1} ---")
        model.step()
        
    print("\n[5/5] Final Simulation Summary")
    # Fetch final stats from DB to verify end-to-end functionality
    with sqlite3.connect("db/observatory.db") as conn:
        cursor = conn.cursor()
        opps = cursor.execute("SELECT COUNT(*) FROM Opportunities").fetchone()[0]
        classified = cursor.execute("SELECT COUNT(*) FROM Opportunities WHERE classified=1").fetchone()[0]
        clusters = cursor.execute("SELECT COUNT(DISTINCT cluster_id) FROM OpportunityClusters").fetchone()[0]
        recs = cursor.execute("SELECT COUNT(*) FROM Recommendations").fetchone()[0]
        notifs = cursor.execute("SELECT COUNT(*) FROM Notifications").fetchone()[0]
        
    print("\n" + "="*40)
    print(f"Opportunities Collected: {opps}")
    print(f"Opportunities Classified: {classified}")
    print(f"Clusters Formed: {clusters}")
    print(f"Recommendations Made: {recs}")
    print(f"Notifications Sent: {notifs}")
    print("="*40 + "\n")
    
    print("SUCCESS: The model has finished processing.")
    print("Dashboard ready — run: streamlit run dashboard/app.py")

if __name__ == "__main__":
    main()
