from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class InternshipScraper(BaseScraperAgent):
    """Scrapes LinkedIn and Indeed for internship listings."""
    
    def get_sources(self) -> List[str]:
        return [
            "https://www.linkedin.com/jobs/internship-jobs",
            "https://www.indeed.com/q-internship-jobs.html"
        ]

    def parse(self, html: str) -> List[Dict[str, Any]]:
        # In production, use BeautifulSoup to extract title, company, location, etc.
        # Since these sites require complex rendering, we return empty in the baseline.
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
        # Example dummy parsing:
        # for card in soup.find_all('div', class_='job-card'):
        #     parsed_items.append({...})
        return parsed_items

    def generate_mock_data(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Software Engineering Intern",
                "description": "Join our core infrastructure team to build scalable services.",
                "deadline": "2026-10-15",
                "url": "https://linkedin.com/jobs/view/101",
                "source": "LinkedIn",
                "type": "internship",
                "location": "San Francisco, CA",
                "eligibility": "BSc/MSc in Computer Science"
            },
            {
                "title": "Data Science Summer Intern",
                "description": "Apply machine learning to massive datasets.",
                "deadline": "2026-11-01",
                "url": "https://indeed.com/viewjob?jk=202",
                "source": "Indeed",
                "type": "internship",
                "location": "Remote",
                "eligibility": "PhD/MSc in Statistics or CS"
            },
            {
                "title": "Product Design Internship",
                "description": "Help design the next generation of our mobile app.",
                "deadline": "2026-12-01",
                "url": "https://linkedin.com/jobs/view/303",
                "source": "LinkedIn",
                "type": "internship",
                "location": "New York, NY",
                "eligibility": "Portfolio required"
            },
            {
                "title": "Cybersecurity Intern",
                "description": "Work with our red team to identify vulnerabilities.",
                "deadline": "2026-09-30",
                "url": "https://indeed.com/viewjob?jk=404",
                "source": "Indeed",
                "type": "internship",
                "location": "Austin, TX",
                "eligibility": "Familiarity with network protocols"
            },
            {
                "title": "Hardware Engineering Intern",
                "description": "Assist in testing and prototyping new chip designs.",
                "deadline": "2026-10-20",
                "url": "https://linkedin.com/jobs/view/505",
                "source": "LinkedIn",
                "type": "internship",
                "location": "Seattle, WA",
                "eligibility": "Electrical Engineering majors"
            }
        ]

    def step(self):
        # Leverage the template method from BaseScraperAgent
        count = super().step()
        print(f"[{self.__class__.__name__}] Collected {count} items")
