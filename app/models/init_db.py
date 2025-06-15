from app.models.database import get_connection

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            room_type TEXT NOT NULL,
            status TEXT DEFAULT 'Available'
        )
    """)
    conn.commit()
    conn.close()
