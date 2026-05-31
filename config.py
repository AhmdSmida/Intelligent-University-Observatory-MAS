import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# DB Settings
DB_PATH = BASE_DIR / "db" / "observatory.db"

# Scraping Settings (Intervals in seconds)
SCRAPING_INTERVALS = {
    "internships": 86400, # 24 hours
    "scholarships": 86400,
    "certifications": 604800, # 1 week
    "research_projects": 172800, # 48 hours
}

# Mock Source URLs (used during simulated mock runs)
MOCK_SOURCE_URLS = {
    "internships": ["https://example.com/mock-internships"],
    "scholarships": ["https://example.com/mock-scholarships"],
    "certifications": ["https://example.com/mock-certifications"],
    "research_projects": ["https://example.com/mock-research"],
}

# Real Source URLs (used during live production runs)
REAL_SOURCE_URLS = {
    "internships": [
        "https://www.linkedin.com/jobs/internship-jobs",
        "https://www.indeed.com/q-internship-jobs.html"
    ],
    "scholarships": [
        "https://www.opportunitiescircle.com/scholarships/",
        "https://www.scholars4dev.com/category/scholarships/"
    ],
    "certifications": [
        "https://www.coursera.org/courses?query=free",
        "https://www.edx.org/search?q=free"
    ],
    "research_projects": [
        "https://www.researchgate.net/jobs/research",
        "https://euraxess.ec.europa.eu/jobs/search"
    ],
}
