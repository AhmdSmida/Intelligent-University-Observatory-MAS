from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class CertificationScraper(BaseScraperAgent):
    """Scrapes Coursera and edX for free courses and certifications."""
    
    def get_sources(self) -> List[str]:
        return [
            "https://www.coursera.org/courses?query=free",
            "https://www.edx.org/search?q=free"
        ]

    def parse(self, html: str) -> List[Dict[str, Any]]:
        # Parsing logic for course and certification listings
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
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
