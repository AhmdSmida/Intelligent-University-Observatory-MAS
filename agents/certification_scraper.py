import config
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class CertificationScraper(BaseScraperAgent):
    """Scrapes Coursera and edX for free courses and certifications."""
    
    @property
    def scraper_type(self) -> str:
        return "certifications"
        
    def get_sources(self) -> List[str]:
        if self.mock_mode:
            return config.MOCK_SOURCE_URLS.get("certifications", [])
        return config.REAL_SOURCE_URLS.get("certifications", [])

    def parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
        
        for card in soup.find_all(['li', 'div'], class_=lambda c: c and ('card' in c.lower() or 'course' in c.lower() or 'result' in c.lower())):
            try:
                title_elem = card.find(['h2', 'h3', 'a'])
                link_elem = card.find('a', href=True)
                
                if title_elem and link_elem and len(title_elem.get_text(strip=True)) > 5:
                    url = link_elem['href']
                    if url.startswith('/'):
                        url = "https://www.coursera.org" + url
                        
                    parsed_items.append({
                        "title": title_elem.get_text(strip=True),
                        "description": "Professional Certification or Course.",
                        "deadline": "2099-12-31",
                        "url": url,
                        "source": "Coursera/edX",
                        "type": "certification",
                        "location": "Online",
                        "eligibility": "Open to everyone"
                    })
            except Exception as e:
                pass
                
        return parsed_items

    def generate_mock_data(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Machine Learning Specialization",
                "description": "Foundational ML course created by Andrew Ng. Covers neural networks, decision trees, etc.",
                "deadline": "2099-12-31", # Courses often don't have hard deadlines
                "url": "https://www.coursera.org/specializations/machine-learning",
                "source": "Coursera",
                "type": "certification",
                "location": "Online",
                "eligibility": "Open to everyone"
            },
            {
                "title": "CS50's Introduction to Computer Science",
                "description": "Harvard University's introduction to the intellectual enterprises of computer science.",
                "deadline": "2099-12-31",
                "url": "https://www.edx.org/course/introduction-computer-science-harvardx-cs50x",
                "source": "edX",
                "type": "certification",
                "location": "Online",
                "eligibility": "Open to everyone"
            },
            {
                "title": "IBM Data Science Professional Certificate",
                "description": "Kickstart your career in Data Science & ML. Build data science skills, learn Python & SQL.",
                "deadline": "2099-12-31",
                "url": "https://www.coursera.org/professional-certificates/ibm-data-science",
                "source": "Coursera",
                "type": "certification",
                "location": "Online",
                "eligibility": "No prior experience required"
            },
            {
                "title": "Agile Project Management",
                "description": "Learn agile frameworks, scrum methodologies, and sprint planning.",
                "deadline": "2099-12-31",
                "url": "https://www.edx.org/course/agile-project-management",
                "source": "edX",
                "type": "certification",
                "location": "Online",
                "eligibility": "Open to everyone"
            },
            {
                "title": "Google Cloud Architecture",
                "description": "Learn to design, develop, and manage robust, secure, and highly available cloud solutions.",
                "deadline": "2099-12-31",
                "url": "https://www.coursera.org/professional-certificates/gcp-cloud-architect",
                "source": "Coursera",
                "type": "certification",
                "location": "Online",
                "eligibility": "Basic IT knowledge recommended"
            }
        ]

    def step(self):
        count = super().step()
        print(f"[{self.__class__.__name__}] Collected {count} items")
