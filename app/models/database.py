import sqlite3

def get_connection():
    return sqlite3.connect("hotel.db")

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    # Ensure correct 'rooms' table
    try:
        cur.execute("SELECT room_type FROM rooms LIMIT 1")
    except sqlite3.OperationalError:
        cur.execute("DROP TABLE IF EXISTS rooms")
        cur.execute('''
            CREATE TABLE rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT,
                room_type TEXT,
                status TEXT
            )
        ''')

    # Create 'employees' table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT
        )
    ''')

    # Create 'users' table and default user
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cur.execute("SELECT * FROM users WHERE username='muhaddas'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('muhaddas', '1234'))

    conn.commit()
    conn.close()
