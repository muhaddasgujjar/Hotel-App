import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.models.database import get_connection

# Admin credentials (static for now)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


def show_admin_panel():
    # Create login popup window
    login_win = ttk.Toplevel()
    login_win.title("Admin Login")
    login_win.geometry("320x220")
    login_win.resizable(False, False)

    frame = ttk.Frame(login_win, padding=20)
    frame.pack(fill=BOTH, expand=True)

    ttk.Label(frame, text="Admin Username").pack(pady=5)
    username_entry = ttk.Entry(frame)
    username_entry.pack(pady=5)

    ttk.Label(frame, text="Password").pack(pady=5)
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    def authenticate():
        username = username_entry.get()
        password = password_entry.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            login_win.destroy()
            open_admin_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid admin credentials.")

    ttk.Button(frame, text="Login", command=authenticate, bootstyle="primary").pack(pady=10)


def open_admin_dashboard():
    # Create admin dashboard
    admin_win = ttk.Toplevel()
    admin_win.title("Admin Dashboard - Room Status")
    admin_win.geometry("700x400")
    admin_win.resizable(True, True)

    ttk.Label(admin_win, text="🛏️ Current Room Bookings", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Create treeview for room data
    columns = ("ID", "Name", "Room", "Checkin", "Checkout")
    tree = ttk.Treeview(admin_win, columns=columns, show="headings", bootstyle="info")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def load_data():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rooms")
        rows = cur.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", END, values=row)

    # Initial load
    load_data()

    # Refresh button
    ttk.Button(admin_win, text="🔄 Refresh", command=load_data, bootstyle="secondary").pack(pady=8)
