import sqlite3

DB_FILE = "posts.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Agar purana table hai toh delete kar do
    cursor.execute("DROP TABLE IF EXISTS posts")

    # Naya table create karo with url column
    cursor.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tag TEXT,
            length TEXT,
            language TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_post(content, tag, length, language, url=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (content, tag, length, language, url)
        VALUES (?, ?, ?, ?, ?)
    ''', (content, tag, length, language, url))
    conn.commit()
    conn.close()


def get_all_posts():
    """Fetch all posts from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_all_posts():
    """Delete all posts (use carefully)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
