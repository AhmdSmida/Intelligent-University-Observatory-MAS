import config
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class ScholarshipScraper(BaseScraperAgent):
    """Scrapes opportunitiescircle.com and scholars4dev.com for scholarships."""
    
    @property
    def scraper_type(self) -> str:
        return "scholarships"
        
    def get_sources(self) -> List[str]:
        if self.mock_mode:
            return config.MOCK_SOURCE_URLS.get("scholarships", [])
        return config.REAL_SOURCE_URLS.get("scholarships", [])

    def parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
        
        # Parse typical WordPress blog posts (scholars4dev, opportunitiescircle)
        for post in soup.find_all(['article', 'div'], class_=lambda c: c and ('post' in c or 'type-post' in c or 'entry' in c)):
            try:
                title_elem = post.find(['h2', 'h3', 'a'])
                desc_elem = post.find(['div', 'p'], class_=lambda c: c and ('excerpt' in c or 'content' in c))
                link_elem = post.find('a', href=True)
                
                if title_elem and link_elem:
                    parsed_items.append({
                        "title": title_elem.get_text(strip=True),
                        "description": desc_elem.get_text(strip=True)[:200] + "..." if desc_elem else "Scholarship opportunity",
                        "deadline": "2026-12-31",
                        "url": link_elem['href'],
                        "source": "Scholarship Web",
                        "type": "scholarship",
                        "location": "Global",
                        "eligibility": "Students / Researchers"
                    })
            except Exception as e:
                pass
                
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
