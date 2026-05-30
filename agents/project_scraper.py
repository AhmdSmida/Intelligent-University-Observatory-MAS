from typing import List, Dict, Any
from bs4 import BeautifulSoup
from agents.base_scraper import BaseScraperAgent

class ProjectScraper(BaseScraperAgent):
    """Scrapes researchgate.net and euraxess.eu for research projects."""
    
    def get_sources(self) -> List[str]:
        return [
            "https://www.researchgate.net/jobs/research",
            "https://euraxess.ec.europa.eu/jobs/search"
        ]

    def parse(self, html: str) -> List[Dict[str, Any]]:
        # Parsing logic for research project listings
        soup = BeautifulSoup(html, 'html.parser')
        parsed_items = []
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
