import sqlite3
import os

# Use a DB path relative to this file so running scripts from other CWDs is safe
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'practice.db')

# If a DB already exists we will migrate in-place to preserve practice data
# (including `practice_sessions`). Do not delete the DB automatically.

# Connect to (or create) the database
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Enable foreign key enforcement for migration operations
cur.execute("PRAGMA foreign_keys = ON;")

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);
""")




# Ensure piano_works exists (needed for foreign key references)
cur.execute("""
CREATE TABLE IF NOT EXISTS piano_works (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    composer TEXT,
    title TEXT
);
""")


cur.execute("""
    CREATE TABLE IF NOT EXISTS user_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        piece_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'in-progress',
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (piece_id) REFERENCES piano_works(id),
        UNIQUE(user_id, piece_id)
    );
    """)
            

cur.execute("""
CREATE TABLE IF NOT EXISTS practice_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    minutes INTEGER NOT NULL CHECK (minutes >= 0),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES user_projects(id) ON DELETE CASCADE
);
""")

cur.execute("PRAGMA foreign_keys = ON")

conn.commit()
conn.close()

print("Database initialized!")

# Create a unique index on username to enforce uniqueness (case-insensitive)
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username COLLATE NOCASE)")
    conn.commit()
finally:
    conn.close()

print("Unique index ensured on users.username")


