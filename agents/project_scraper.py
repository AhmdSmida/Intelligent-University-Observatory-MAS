import config
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class ProjectScraper(BaseScraperAgent):
    """Scrapes researchgate.net and euraxess.eu for research projects."""
    
    @property
    def scraper_type(self) -> str:
        return "research_projects"
        
    def get_sources(self) -> List[str]:
        if self.mock_mode:
            return config.MOCK_SOURCE_URLS.get("research_projects", [])
        return config.REAL_SOURCE_URLS.get("research_projects", [])

    def parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
        
        for card in soup.find_all(['div', 'li', 'article'], class_=lambda c: c and ('job' in c.lower() or 'item' in c.lower() or 'card' in c.lower())):
            try:
                title_elem = card.find(['h2', 'h3', 'a'])
                loc_elem = card.find(['div', 'span'], class_=lambda c: c and 'location' in c.lower())
                link_elem = card.find('a', href=True)
                
                if title_elem and link_elem and len(title_elem.get_text(strip=True)) > 5:
                    url = link_elem['href']
                    if url.startswith('/'):
                        url = "https://www.researchgate.net" + url
                        
                    parsed_items.append({
                        "title": title_elem.get_text(strip=True),
                        "description": "Research project opportunity.",
                        "deadline": "2026-12-31",
                        "url": url,
                        "source": "Research Portal",
                        "type": "research",
                        "location": loc_elem.get_text(strip=True) if loc_elem else "Global",
                        "eligibility": "Academic Researchers"
                    })
            except Exception as e:
                pass
                
        return parsed_items

    def generate_mock_data(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Quantum Computing Postdoc Research",
                "description": "Investigate fault-tolerant quantum error correction codes.",
                "deadline": "2026-08-30",
                "url": "https://www.researchgate.net/job/1001",
                "source": "ResearchGate",
                "type": "research",
                "location": "Zurich, Switzerland",
                "eligibility": "PhD in Physics or related field"
            },
            {
                "title": "Horizon Europe: Green Energy Integration",
                "description": "Develop scalable solutions for integrating renewable energy into existing grids.",
                "deadline": "2026-09-15",
                "url": "https://euraxess.ec.europa.eu/jobs/2002",
                "source": "EURAXESS",
                "type": "research",
                "location": "Berlin, Germany",
                "eligibility": "Researchers with 3+ years experience"
            },
            {
                "title": "Bioinformatics Sequence Analysis",
                "description": "Work on genomic sequence alignment algorithms for rare diseases.",
                "deadline": "2026-07-31",
                "url": "https://www.researchgate.net/job/1003",
                "source": "ResearchGate",
                "type": "research",
                "location": "Boston, MA",
                "eligibility": "Strong programming and biology background"
            },
            {
                "title": "Marie Skłodowska-Curie Actions Fellowship",
                "description": "Prestigious fellowship supporting researchers at all stages of their careers.",
                "deadline": "2026-10-12",
                "url": "https://euraxess.ec.europa.eu/jobs/2004",
                "source": "EURAXESS",
                "type": "research",
                "location": "Across Europe",
                "eligibility": "Doctoral degree required"
            },
            {
                "title": "AI in Medical Imaging",
                "description": "Apply deep learning techniques to detect early signs of Alzheimer's in MRI scans.",
                "deadline": "2026-08-15",
                "url": "https://www.researchgate.net/job/1005",
                "source": "ResearchGate",
                "type": "research",
                "location": "London, UK",
                "eligibility": "Experience with PyTorch/TensorFlow"
            }
        ]

    def step(self):
        count = super().step()
        print(f"[{self.__class__.__name__}] Collected {count} items")
