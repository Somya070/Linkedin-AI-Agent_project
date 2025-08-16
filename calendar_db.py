import sqlite3

# ===== CREATE TABLE IF NOT EXISTS =====
def init_calendar_db():
    conn = sqlite3.connect("content_calendar.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calendar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL,
                    status TEXT DEFAULT 'Planned'
                )''')
    conn.commit()
    conn.close()

# ===== ADD NEW ENTRY =====
def add_calendar_entry(title, description, date, status="Planned"):
    conn = sqlite3.connect("content_calendar.db")
    c = conn.cursor()
    c.execute("INSERT INTO calendar (title, description, date, status) VALUES (?, ?, ?, ?)",
              (title, description, date, status))
    conn.commit()
    conn.close()

# ===== GET ALL ENTRIES =====
def get_all_entries():
    conn = sqlite3.connect("content_calendar.db")
    c = conn.cursor()
    c.execute("SELECT * FROM calendar ORDER BY date ASC")
    rows = c.fetchall()
    conn.close()
    return rows

# ===== UPDATE STATUS =====
def update_status(entry_id, new_status):
    conn = sqlite3.connect("content_calendar.db")
    c = conn.cursor()
    c.execute("UPDATE calendar SET status = ? WHERE id = ?", (new_status, entry_id))
    conn.commit()
    conn.close()

# ===== DELETE ENTRY =====
def delete_entry(entry_id):
    conn = sqlite3.connect("content_calendar.db")
    c = conn.cursor()
    c.execute("DELETE FROM calendar WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

from calendar_db import init_calendar_db, add_calendar_entry, get_all_entries, update_status, delete_entry

# Initialize database
init_calendar_db()

# Add sample entries
add_calendar_entry("Post on LinkedIn AI Agent", "A summary of new LinkedIn AI Agent feature", "2025-08-15")
add_calendar_entry("Instagram Reel: Self Development", "Quick tips for confidence", "2025-08-16")

# Show all entries
print("📅 Content Calendar:")
for entry in get_all_entries():
    print(entry)

# Update status of first entry
update_status(1, "Completed")