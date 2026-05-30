from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class ScholarshipScraper(BaseScraperAgent):
    """Scrapes opportunitiescircle.com and scholars4dev.com for scholarships."""
    
    def get_sources(self) -> List[str]:
        return [
            "https://www.opportunitiescircle.com/scholarships/",
            "https://www.scholars4dev.com/category/scholarships/"
        ]

    def parse(self, html: str) -> List[Dict[str, Any]]:
        # Parsing logic for scholarship listings
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
        return parsed_items

    def generate_mock_data(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Global Excellence Scholarship",
                "description": "Full-tuition scholarship for international students demonstrating outstanding academic achievement.",
                "deadline": "2027-01-15",
                "url": "https://www.opportunitiescircle.com/global-excellence",
                "source": "OpportunitiesCircle",
                "type": "scholarship",
                "location": "United Kingdom",
                "eligibility": "International Students, GPA 3.8+"
            },
            {
                "title": "Women in Tech STEM Grant",
                "description": "$10,000 grant to support women pursuing degrees in Computer Science and Engineering.",
                "deadline": "2026-11-30",
                "url": "https://www.scholars4dev.com/women-in-tech",
                "source": "Scholars4Dev",
                "type": "scholarship",
                "location": "Global",
                "eligibility": "Female applicants in STEM"
            },
            {
                "title": "Future Leaders Fellowship",
                "description": "Provides funding and mentorship for graduate students researching climate change.",
                "deadline": "2026-10-01",
                "url": "https://www.opportunitiescircle.com/future-leaders",
                "source": "OpportunitiesCircle",
                "type": "scholarship",
                "location": "Australia",
                "eligibility": "Graduate students"
            },
            {
                "title": "Eiffel Excellence Scholarship",
                "description": "Developed by the French Ministry to attract top foreign students for master's and PhD.",
                "deadline": "2027-02-10",
                "url": "https://www.scholars4dev.com/eiffel",
                "source": "Scholars4Dev",
                "type": "scholarship",
                "location": "France",
                "eligibility": "Under 25 (Masters), Under 30 (PhD)"
            },
            {
                "title": "Developing Nations Academic Fund",
                "description": "Covers living expenses and tuition for students from developing countries.",
                "deadline": "2026-12-15",
                "url": "https://www.opportunitiescircle.com/developing-nations",
                "source": "OpportunitiesCircle",
                "type": "scholarship",
                "location": "Canada",
                "eligibility": "Citizens of designated developing nations"
            }
        ]

    def step(self):
        count = super().step()
        print(f"[{self.__class__.__name__}] Collected {count} items")
