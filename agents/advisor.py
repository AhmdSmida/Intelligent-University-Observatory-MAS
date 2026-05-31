import sqlite3
import logging
from collections import defaultdict
from mesa import Agent

class AgentAdvisor(Agent):
    """
    AgentAdvisor acts as the student's personal career counselor.
    It queries high-scoring recommendations, groups them logically by category,
    formats them into a beautiful ranked suggestion list, and marks them as sent.
    """
    
    def __init__(self, model):
        super().__init__(model)
        self.logger = logging.getLogger(self.__class__.__name__)

    def step(self):
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Query Recommendations, limiting to unsent and sorting by highest score
                cursor.execute('''
                    SELECT r.id, r.user_id, u.name, r.opportunity_id, o.title, o.category, r.score 
                    FROM Recommendations r
                    JOIN Users u ON r.user_id = u.id
                    JOIN Opportunities o ON r.opportunity_id = o.id
                    WHERE r.sent = 0
                    ORDER BY r.user_id, r.score DESC
                ''')
                rows = cursor.fetchall()
                
                if not rows:
                    self.logger.info("No new unsent recommendations to advise on.")
                    return
                
                # Group all recommendations by user
                user_recs = defaultdict(list)
                for row in rows:
                    rec_id, user_id, user_name, opp_id, title, category, score = row
                    user_recs[user_name].append({
                        "rec_id": rec_id,
                        "title": title,
                        "category": category,
                        "score": score
                    })
                
                marked_sent_ids = []
                
                # 2. Format a ranked suggestion list to the console
                print("\n" + "="*60)
                print("ADVISOR AGENT: PERSONALIZED WEEKLY DIGEST".center(60))
                print("="*60)
                
                for user_name, recs in user_recs.items():
                    # Keep only the top 10 best matches per user
                    top_10 = recs[:10]
                    
                    print(f"\n*** PREPARED FOR: {user_name.upper()} ***")
                    
                    # 3. Group recommendations by category
                    cat_groups = defaultdict(list)
                    for rec in top_10:
                        cat_groups[rec['category']].append(rec)
                        marked_sent_ids.append((rec['rec_id'],))
                        
                    for category, items in cat_groups.items():
                        # Fallback for missing category strings
                        cat_name = str(category).replace("_", " ").upper() if category else "UNCATEGORIZED"
                        print(f"  -> {cat_name}:")
                        
                        for item in items:
                            # Convert 0.0-1.0 score to a nice percentage
                            score_pct = int(item['score'] * 100)
                            print(f"     - {item['title']} (Match: {score_pct}%)")
                            
                print("\n" + "="*60 + "\n")
                
                # 4. Mark all logged recommendations as "sent=True"
                cursor.executemany("UPDATE Recommendations SET sent = 1 WHERE id = ?", marked_sent_ids)
                conn.commit()
                
                self.logger.info(f"Advised on {len(marked_sent_ids)} recommendations and marked them as sent.")
                
        except Exception as e:
            self.logger.error(f"Error in Advisor Agent: {e}")
