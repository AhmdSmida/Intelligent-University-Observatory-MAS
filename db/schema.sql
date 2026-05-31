CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    skills TEXT, -- comma-separated
    interests TEXT, -- comma-separated
    academic_level TEXT
);

CREATE TABLE IF NOT EXISTS Opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL, -- 'internship', 'scholarship', 'certification', 'research'
    title TEXT NOT NULL,
    description TEXT,
    url TEXT UNIQUE NOT NULL,
    deadline DATE,
    source TEXT,
    location TEXT,
    eligibility TEXT,
    classified BOOLEAN DEFAULT 0,
    category TEXT,
    tags TEXT,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS OpportunityClusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cluster_id INTEGER NOT NULL,
    cluster_name TEXT NOT NULL,
    opportunity_id INTEGER UNIQUE,
    FOREIGN KEY(opportunity_id) REFERENCES Opportunities(id)
);

CREATE TABLE IF NOT EXISTS Recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    opportunity_id INTEGER,
    score REAL,
    sent BOOLEAN DEFAULT 0,
    date_recommended DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(opportunity_id) REFERENCES Opportunities(id)
);

CREATE TABLE IF NOT EXISTS Notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    opportunity_id INTEGER,
    status TEXT DEFAULT 'pending',
    date_sent DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(opportunity_id) REFERENCES Opportunities(id)
);


-- Removed hardcoded sample Recommendations and Notifications
-- The MAS will generate these organically based on the new class profiles!
