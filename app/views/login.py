import ttkbootstrap as ttk
from tkinter import messagebox
from app.models.database import get_connection
from app.views.dashboard import open_dashboard

def show_login():
    win = ttk.Window(themename="solar")
    win.title("Login")
    win.geometry("400x300")

    ttk.Label(win, text="Username:").pack(pady=10)
    username_entry = ttk.Entry(win, width=30)
    username_entry.pack()

    ttk.Label(win, text="Password:").pack(pady=10)
    password_entry = ttk.Entry(win, show="*", width=30)
    password_entry.pack()

    def validate_login():
        user = username_entry.get()
        pwd = password_entry.get()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = cur.fetchone()
        conn.close()

        if result:
            open_dashboard(win, user)  # 👈 Pass login window to destroy
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Renter password")

    ttk.Button(win, text="Login", command=validate_login, bootstyle="success").pack(pady=20)
    win.mainloop()
