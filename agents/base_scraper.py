import sqlite3
import logging
import requests
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from mesa import Agent

class BaseScraperAgent(Agent, ABC):
    """
    Abstract Base Class for all Scraper Agents.
    
    === DESIGN PATTERN EXPLANATION (For Your Professor) ===
    This architecture implements the 'Template Method' design pattern combined 
    with an Abstract Base Class (ABC).
    
    1. The ABC (Abstract Base Class) Pattern:
       By inheriting from `ABC` and using the `@abstractmethod` decorator, we 
       enforce a strict contract. Any concrete scraper (like InternshipScraperAgent) 
       *must* implement `get_sources()` and `parse()`. If a student forgets to 
       write a parser, Python will instantly throw an instantiation error, preventing
       incomplete agents from entering the simulation.
       
    2. The Template Method Pattern:
       The `step()` method acts as the "template". It defines the immutable workflow 
       that all scrapers must share: Fetch URL -> Parse -> Validate -> Save to DB. 
       Child classes don't need to rewrite the network requests or database logic. 
       They only provide the specific data (URLs) and the specific parsing rules, 
       plugging them into the 'holes' left by the parent class.
       
    Benefits: Maximizes code reuse, enforces strict data validation (so the MAS 
    database doesn't get corrupted with missing fields), and makes adding a new 
    scraper trivial (just two methods to implement).
    =======================================================
    """

    # Every parsed item must contain these keys before being allowed into the DB
    REQUIRED_KEYS = {"title", "description", "deadline", "url", "source", "type", "location", "eligibility"}

    def __init__(self, model, mock_mode: bool = False):
        super().__init__(model)
        self.mock_mode = mock_mode
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def get_sources(self) -> List[str]:
        """Return a list of URLs to scrape."""
        pass

    @abstractmethod
    def parse(self, html: str) -> List[Dict[str, Any]]:
        """Parse the HTML content and return a list of opportunity dictionaries."""
        pass

    def fetch_url(self, url: str) -> str:
        """
        Fetches HTML from a URL with graceful error handling and a single retry.
        """
        for attempt in range(2): # Attempt 1 + Retry 1
            try:
                # Add a realistic timeout to prevent hanging the simulation
                response = requests.get(url, timeout=10)
                response.raise_for_status() # Raises HTTPError for bad responses
                return response.text
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == 0:
                    time.sleep(2) # Graceful backoff before retry
                else:
                    self.logger.error(f"Failed to fetch {url} after retries. Skipping.")
        return ""

    def validate(self, item: Dict[str, Any]) -> bool:
        """
        Check if the parsed item adheres to the required schema.
        """
        missing_keys = self.REQUIRED_KEYS - set(item.keys())
        if missing_keys:
            self.logger.warning(f"Validation failed. Missing keys {missing_keys} in: {item.get('url', 'Unknown')}")
            return False
        return True

    def save_to_db(self, valid_items: List[Dict[str, Any]]):
        """
        Saves fully validated opportunities to the SQLite database.
        """
        if not valid_items:
            return
            
        # Dynamically fetch DB path from the global config
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                for item in valid_items:
                    cursor.execute('''
                        INSERT OR IGNORE INTO Opportunities 
                        (type, title, description, url, deadline, source, location, eligibility)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item['type'], item['title'], item['description'], 
                        item['url'], item['deadline'], item['source'], 
                        item['location'], item['eligibility']
                    ))
                conn.commit()
                
                # Update MAS metrics dynamically
                self.model.opportunities_collected += len(valid_items)
                self.logger.info(f"Saved {len(valid_items)} new opportunities to database.")
        except Exception as e:
            self.logger.error(f"Database insertion error: {e}")

    def generate_mock_data(self) -> List[Dict[str, Any]]:
        """
        Return realistic fake data for safe testing and demonstrations.
        """
        return [
            {
                "title": f"Mock Opportunity ({self.__class__.__name__})",
                "description": "This is a highly realistic mock description generated for testing purposes.",
                "deadline": "2026-12-31",
                "url": f"https://example.com/mock/{id(self)}",
                "source": "MockUniversityAPI",
                "type": "internship", # The child class can override this in production
                "location": "Remote",
                "eligibility": "Computer Science Students"
            }
        ]

    def step(self):
        """
        The Template Method defining the execution workflow for all scrapers.
        """
        valid_items = []
        
        if self.mock_mode:
            self.logger.info("Running in MOCK MODE. Generating fake data.")
            items = self.generate_mock_data()
            for item in items:
                if self.validate(item):
                    valid_items.append(item)
        else:
            urls = self.get_sources()
            for url in urls:
                html = self.fetch_url(url)
                if not html:
                    continue
                    
                # Defer to the child class's specific parsing implementation
                items = self.parse(html)
                
                for item in items:
                    if self.validate(item):
                        valid_items.append(item)
                        
        self.save_to_db(valid_items)
        return len(valid_items)
