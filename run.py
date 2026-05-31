import os
import sqlite3
import subprocess
import time
from model import ObservatoryModel

def init_db(mock_mode: bool):
    print("\n[1/5] Initializing Database...")
    db_path = "db/observatory.db"
    
    # Always remove existing DB to start fresh and avoid mixing mock/real data
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Database cleared for a fresh run.")
        
    subprocess.run(["python", "db/init_db.py"], check=True)
    print("Database initialized successfully.")

import random

def seed_users():
    print("\n[2/5] Seeding Classmate Profiles...")
    classmates = [
        "ABDELHEDI MOHAMED", "ABIDI MARIEM", "ABIRIGA SEIFALLAH", "ABID RAYEN", "AGREBI OMAR", 
        "AMMAR ISLEM", "AYECH EYA", "BAAZAOUI NOUR EL ISLAM", "BALHOUANE FATMA", "BEN GHAYADHA AYOUB", 
        "BESROUR ABDERAHMEN", "BOUKHRIS ADEM", "CHAOUACHI MOHAMED YASSINE", "CHERIF MOHAMED RAYEN", 
        "DHAFER MOHAMED AMINE", "DRIDI MOHAMED YASSINE", "FEHRI MAZEN", "GUEMRI MOHAMED ANOUER", 
        "HAJLAOUI MOHAMED KHALIL", "HAMDI TAYMA", "HAMMAMI OMAR", "HMADI RAZI", "JEBARI EYA", 
        "JLALI TASNIM", "JRIDI MOHAMED", "KHALAF AYOUB", "KHALAF IBRAHIM", "KAOUACH MOHAMED AZIZ", 
        "LOUSSAIEF MOHAMED HABIB", "MADDOURI RAFEH", "MANSOUR DHIA EDDINE", "MECHEY ADEM", 
        "MEGUEBLI MOHAMED", "MISSAOUI RANIM", "MOSBAHI TAHA ELAMIN", "NEFZI LOUAY", "OUARDYEN YOUSSEF", 
        "OUESLATI THAMEUR", "SELLAMI MERIEM", "SEGHAIER HEJER", "SFAR EYA", "SHILI ISMAIL", 
        "SLIMI LOUAY", "SMIDA AHMED", "TENNICH BRAHIM", "TIOUIRI ABDELHALIM", "TOUZI SENDA", 
        "WALI MOHAMED", "ZAIBI RAYEN", "ZRIGA MERIEM"
    ]
    
    skill_pools = [
        "Python, Machine Learning, Deep Learning", "Java, Spring Boot, SQL", "JavaScript, React, Node.js", 
        "C++, Robotics, ROS", "Data Analysis, SQL, Pandas", "Project Management, Agile, Scrum",
        "Cloud Computing, AWS, Docker", "Bioinformatics, Sequence Analysis, Data", "Cybersecurity, Networking"
    ]
    
    interest_pools = [
        "Data Science Internships", "Web Development, Full Stack", "Research, Quantum Computing",
        "Scholarships, Funding", "Postdoc, Academic Research", "UI/UX, Frontend Design",
        "DevOps, Cloud Architecture", "AI in Healthcare", "Hardware, IoT Engineering"
    ]
    
    levels = ["Undergraduate", "Masters", "PhD", "Postdoc"]
    
    users = []
    for name in classmates:
        email = name.lower().replace(" ", ".") + "@student.uni.edu"
        skills = random.choice(skill_pools)
        interests = random.choice(interest_pools)
        level = random.choice(levels)
        # Title case makes the names look perfectly formatted (e.g., Abidi Mariem)
        users.append((name.title(), email, skills, interests, level))
    
    with sqlite3.connect("db/observatory.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO Users (name, email, skills, interests, academic_level) VALUES (?, ?, ?, ?, ?)", 
            users
        )
        conn.commit()
    print(f"Seeded {len(users)} real classmate profiles into the MAS.")

def main():
    print("="*60)
    print("INTELLIGENT UNIVERSITY OBSERVATORY MAS LAUNCHER".center(60))
    print("="*60)
    
    # Initialize the model with dynamic config
    config = {
        "DB_PATH": "db/observatory.db",
        "SCRAPER_MOCK_MODE": False
    }
    
    init_db(config["SCRAPER_MOCK_MODE"])
    seed_users()
    
    print("\n[3/5] Starting Observatory MAS Model...")
    model = ObservatoryModel(config)
    
    print("\n[4/5] Running Continuous Background MAS Worker...")
    print("Press Ctrl+C at any time to stop the worker.")
    
    step = 1
    try:
        while True:
            print(f"\n--- EXECUTING SIMULATION STEP {step} ---")
            model.step()
            
            # Print intermediate summary so the console stays active
            with sqlite3.connect("db/observatory.db") as conn:
                cursor = conn.cursor()
                opps = cursor.execute("SELECT COUNT(*) FROM Opportunities").fetchone()[0]
                recs = cursor.execute("SELECT COUNT(*) FROM Recommendations").fetchone()[0]
            print(f"Stats: {opps} Opportunities | {recs} Recommendations generated.")
            
            # Sleep logic to prevent 100% CPU usage
            # Since scrapers now track their own 24h intervals in base_scraper.py, 
            # the main loop can run frequently to let internal agents (clusters/matchers) process data instantly.
            sleep_time = 10
                
            print(f"Sleeping for {sleep_time} seconds before next step...\n")
            time.sleep(sleep_time)
            step += 1
            
    except KeyboardInterrupt:
        print("\n\nMAS Worker manually stopped by user.")
        
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
