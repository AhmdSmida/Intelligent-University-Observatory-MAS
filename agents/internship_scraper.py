import config
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class InternshipScraper(BaseScraperAgent):
    """Scrapes LinkedIn and Indeed for internship listings."""
    
    @property
    def scraper_type(self) -> str:
        return "internships"
        
    def get_sources(self) -> List[str]:
        if self.mock_mode:
            return config.MOCK_SOURCE_URLS.get("internships", [])
        return config.REAL_SOURCE_URLS.get("internships", [])

    def parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
        
        # Parse LinkedIn job cards (often found under 'base-card' or 'job-search-card')
        for card in soup.find_all(['div', 'li'], class_=lambda c: c and ('base-card' in c or 'job-search-card' in c)):
            try:
                title_elem = card.find(['h3', 'span'], class_=lambda c: c and 'title' in c.lower())
                company_elem = card.find(['h4', 'a'], class_=lambda c: c and 'subtitle' in c.lower())
                loc_elem = card.find('span', class_=lambda c: c and 'location' in c.lower())
                link_elem = card.find('a', href=True)
                
                if title_elem and link_elem:
                    parsed_items.append({
                        "title": title_elem.get_text(strip=True),
                        "description": f"Internship at {company_elem.get_text(strip=True) if company_elem else 'Unknown Company'}",
                        "deadline": "2026-12-31", # LinkedIn often hides deadlines
                        "url": link_elem['href'],
                        "source": "LinkedIn",
                        "type": "internship",
                        "location": loc_elem.get_text(strip=True) if loc_elem else "Remote",
                        "eligibility": "Undergraduate / Graduate"
                    })
            except Exception as e:
                pass
                
        # Parse Indeed job cards (often 'job_seen_beacon' or 'result')
        for card in soup.find_all(['div', 'td'], class_=lambda c: c and ('job_seen_beacon' in c or 'result' in c)):
            try:
                title_elem = card.find(['h2', 'span'], class_=lambda c: c and 'title' in c.lower())
                company_elem = card.find('span', class_=lambda c: c and 'company' in c.lower())
                loc_elem = card.find('div', class_=lambda c: c and 'location' in c.lower())
                link_elem = card.find('a', href=True)
                
                if title_elem and link_elem:
                    parsed_items.append({
                        "title": title_elem.get_text(strip=True),
                        "description": f"Internship at {company_elem.get_text(strip=True) if company_elem else 'Unknown Company'}",
                        "deadline": "2026-12-31",
                        "url": "https://indeed.com" + link_elem['href'] if link_elem['href'].startswith('/') else link_elem['href'],
                        "source": "Indeed",
                        "type": "internship",
                        "location": loc_elem.get_text(strip=True) if loc_elem else "Remote",
                        "eligibility": "Undergraduate / Graduate"
                    })
            except Exception as e:
                pass

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
