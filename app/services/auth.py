from app.models.database import get_connection

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None
# app/services/auth.py

def check_credentials(username, password):
    return username == "muhaddas" and password == "12345"
