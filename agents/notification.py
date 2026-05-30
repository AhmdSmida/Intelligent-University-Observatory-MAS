import sqlite3
import logging
from mesa import Agent

class AgentNotification(Agent):
    """
    AgentNotification acts as the system's Watchdog, monitoring impending deadlines 
    and dispatching alerts to relevant students.
    
    === Why Notification Agents are a Common Pattern in MAS ===
    In a true Multi-Agent System, we heavily rely on the "Separation of Concerns" principle. 
    Rather than making every scraper or matcher constantly poll the environment to 
    see if a deadline is approaching, we isolate this temporal logic into a specialized 
    Notification Agent.
    
    This pattern drastically reduces system overhead. The Notification Agent is the 
    *only* entity responsible for evaluating time. It sleeps, wakes up asynchronously, 
    checks deadlines globally, and dispatches messages to users. It acts as a decoupled, 
    event-driven publisher in a publish-subscribe architecture!
    """
    
    def __init__(self, model):
        super().__init__(model)
        self.logger = logging.getLogger(self.__class__.__name__)

    def step(self):
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Load opportunities with a deadline in the next 7 days
                # We use SQLite's native date functions to find impending deadlines
                cursor.execute('''
                    SELECT id, title, deadline, CAST(julianday(deadline) - julianday('now') AS INTEGER) as days_left 
                    FROM Opportunities 
                    WHERE deadline IS NOT NULL 
                    AND julianday(deadline) - julianday('now') BETWEEN 0 AND 7
                ''')
                
                imminent_opps = cursor.fetchall()
                
                if not imminent_opps:
                    self.logger.info("No deadlines approaching in the next 7 days.")
                    return
                    
                notifications_to_insert = []
                
                print("\n" + "!"*10 + " DEADLINE ALERTS " + "!"*10)
                
                # 2. For each opportunity, find users who were recommended this opportunity
                for opp_id, title, deadline_str, days_left in imminent_opps:
                    cursor.execute('''
                        SELECT u.id, u.name 
                        FROM Recommendations r
                        JOIN Users u ON r.user_id = u.id
                        WHERE r.opportunity_id = ?
                    ''', (opp_id,))
                    
                    users_to_notify = cursor.fetchall()
                    
                    for user_id, user_name in users_to_notify:
                        # Prevent duplicate alerts if they already have a pending one
                        cursor.execute('''
                            SELECT id FROM Notifications 
                            WHERE user_id = ? AND opportunity_id = ? AND status = 'pending'
                        ''', (user_id, opp_id))
                        
                        if not cursor.fetchone():
                            # 3. Create a pending Notification row
                            notifications_to_insert.append((user_id, opp_id, "pending"))
                            # 4. Print alert to console
                            print(f"ALERT: {user_name} — {title} — deadline in {days_left} days")
                
                if notifications_to_insert:
                    cursor.executemany('''
                        INSERT INTO Notifications (user_id, opportunity_id, status, date_sent)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    ''', notifications_to_insert)
                    
                    conn.commit()
                    self.logger.info(f"Inserted {len(notifications_to_insert)} new deadline notifications.")
                else:
                    self.logger.info("No new alerts needed (alerts already sent).")
                    
                print("="*40 + "\n")
                
        except Exception as e:
            self.logger.error(f"Error in Notification Agent: {e}")

    def mark_seen(self, notification_id: int):
        """
        Updates the status of a specific notification to 'seen'.
        In a real app, the Streamlit dashboard would trigger this when a user clicks the alert.
        """
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE Notifications SET status = 'seen' WHERE id = ?", (notification_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Notification ID {notification_id} marked as seen.")
                else:
                    self.logger.warning(f"Notification ID {notification_id} not found.")
                    
        except Exception as e:
            self.logger.error(f"Error marking notification seen: {e}")
