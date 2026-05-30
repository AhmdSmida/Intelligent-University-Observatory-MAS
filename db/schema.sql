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
    opportunity_id INTEGER,
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

-- Insert sample Users
INSERT INTO Users (name, email, skills, interests, academic_level) VALUES
('Alice Smith', 'alice@student.uni.edu', 'Python, Data Analysis', 'Machine Learning, Internships', 'Undergraduate'),
('Bob Johnson', 'bob@student.uni.edu', 'Java, Spring Boot', 'Web Development, Scholarships', 'Masters'),
('Charlie Brown', 'charlie@student.uni.edu', 'C++, Robotics', 'Research, Hardware', 'PhD'),
('Diana Prince', 'diana@student.uni.edu', 'Project Management, Agile', 'Certifications, Leadership', 'Masters'),
('Evan Wright', 'evan@student.uni.edu', 'JavaScript, React', 'Frontend, UI/UX', 'Undergraduate');

-- Insert sample Opportunities
INSERT INTO Opportunities (type, title, description, url, deadline) VALUES
('internship', 'Data Science Intern', 'Summer internship focusing on predictive modeling.', 'https://example.com/intern/ds', date('now', '+3 days')),
('scholarship', 'Merit Scholarship for Tech Students', '$5000 scholarship for top CS students.', 'https://example.com/schol/merit', date('now', '+15 days')),
('certification', 'Cloud Practitioner Cert', 'Foundational cloud computing certification.', 'https://example.com/cert/cloud', NULL),
('research', 'AI in Healthcare Research Assistant', 'Assist with analyzing medical image datasets.', 'https://example.com/res/ai-health', date('now', '+5 days')),
('internship', 'Frontend Developer Intern', 'Help build our new web dashboard.', 'https://example.com/intern/fe', '2026-07-15');

-- Insert sample OpportunityClusters
INSERT INTO OpportunityClusters (cluster_id, cluster_name, opportunity_id) VALUES
(1, 'Data & AI', 1),
(2, 'Financial Aid', 2),
(3, 'Cloud Computing', 3),
(1, 'Data & AI', 4),
(4, 'Web Dev', 5);

-- Insert sample Recommendations
INSERT INTO Recommendations (user_id, opportunity_id, score) VALUES
(1, 1, 0.95),
(1, 4, 0.88),
(2, 5, 0.92),
(2, 2, 0.85),
(3, 4, 0.90);

-- Insert sample Notifications
INSERT INTO Notifications (user_id, opportunity_id, status) VALUES
(1, 1, 'pending'),
(2, 2, 'seen'),
(3, 4, 'pending'),
(4, 3, 'pending'),
(5, 5, 'pending');
