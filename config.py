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

# Source URLs
SOURCE_URLS = {
    "internships": ["https://example.com/internships"],
    "scholarships": ["https://example.com/scholarships"],
    "certifications": ["https://example.com/certifications"],
    "research_projects": ["https://example.com/research"],
}
