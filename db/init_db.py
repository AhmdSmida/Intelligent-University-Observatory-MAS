import sqlite3
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import DB_PATH

def init_db():
    schema_path = Path(__file__).parent / 'schema.sql'
    
    # Ensure db directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as conn:
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
    print(f"Database initialized successfully at {DB_PATH}")

if __name__ == '__main__':
    init_db()
