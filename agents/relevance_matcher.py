import sqlite3
import logging
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from mesa import Agent

class AgentRelevanceMatcher(Agent):
    """
    AgentRelevanceMatcher maps user profiles to opportunities using cosine similarity.
    
    === How Cosine Similarity Works (Intuitive Explanation) ===
    Imagine an N-dimensional space, where each dimension represents a specific word 
    (like "Python", "Data", "Scholarship", "PhD"). 
    
    1. A document (like an opportunity description or a student's profile) is plotted 
       as a line (vector) pointing outward from the origin in this space. The direction 
       the line points is determined by which words the document contains.
       
    2. Cosine similarity measures the ANGLE between two vectors. 
       - If they share many important words, they point in roughly the same direction, 
         making the angle very small, and the cosine score close to 1.0 (a perfect match).
       - If they share zero words, they point 90 degrees apart, and the cosine is 0.0.
       
    Why is this brilliant for matching students to jobs? Because it ignores the LENGTH 
    of the document! A student's profile might be just 5 words ("Python Data PhD Machine Learning"), 
    while an internship description might be 500 words long. Because cosine similarity 
    only looks at the *angle* (the relative proportion of matching words), it correctly 
    identifies them as a perfect match without penalizing the student's short profile!
    """
    
    def __init__(self, model):
        super().__init__(model)
        self.logger = logging.getLogger(self.__class__.__name__)

    def step(self):
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Load users with their academic levels
                cursor.execute("SELECT id, skills, interests, academic_level FROM Users")
                users = cursor.fetchall()
                if not users:
                    self.logger.warning("No users found in database.")
                    return
                
                # 2. Load classified opportunities
                # We only match against opportunities that have passed the Classifier Agent
                cursor.execute("SELECT id, title, description, category, tags FROM Opportunities WHERE classified = 1")
                opportunities = cursor.fetchall()
                if not opportunities:
                    self.logger.warning("No classified opportunities found.")
                    return
                
                # Create a rich text representation of the opportunity
                opp_ids = [opp[0] for opp in opportunities]
                opp_texts = [f"{opp[1]} {opp[2]} {opp[3]} {opp[4]}" for opp in opportunities]
                
                # 3. Vectorize Opportunities using TF-IDF
                vectorizer = TfidfVectorizer(stop_words='english')
                opp_tfidf = vectorizer.fit_transform(opp_texts)
                
                updates = []
                
                # 4. Compare every user against all opportunities
                for user_id, skills, interests, academic_level in users:
                    # Construct a dense user profile text string
                    user_text = f"{skills or ''} {interests or ''} {academic_level or ''}"
                    
                    if not user_text.strip():
                        continue
                        
                    # Vectorize the user's profile using the EXACT SAME vectorizer space
                    user_tfidf = vectorizer.transform([user_text])
                    
                    # 5. Compute cosine similarity between this 1 user and ALL opportunities simultaneously
                    scores = cosine_similarity(user_tfidf, opp_tfidf)[0]
                    
                    # 6. Filter and prepare database inserts for good matches
                    for idx, score in enumerate(scores):
                        if score > 0.3: # Threshold
                            updates.append((user_id, opp_ids[idx], float(score)))
                            
                # 7. Save to Recommendations table
                # We use REPLACE/IGNORE logic implicitly or just insert since this is a demo.
                # In production, we would check if a recommendation already exists.
                cursor.executemany('''
                    INSERT INTO Recommendations (user_id, opportunity_id, score, sent)
                    VALUES (?, ?, ?, 0)
                ''', updates)
                
                conn.commit()
                
                # Update system metrics
                self.model.recommendations_made += len(updates)
                self.logger.info(f"RelevanceMatcher generated {len(updates)} highly personalized recommendations.")
                
        except Exception as e:
            self.logger.error(f"Error in RelevanceMatcher: {e}")
