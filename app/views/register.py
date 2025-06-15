import ttkbootstrap as ttk
from tkinter import messagebox
from app.models.database import get_connection

def show_register_window():
    win = ttk.Toplevel()
    win.title("Register")
    win.geometry("300x250")
    win.resizable(False, False)

    ttk.Label(win, text="Register", font=("Helvetica", 16)).pack(pady=10)

    ttk.Label(win, text="Username").pack()
    username_entry = ttk.Entry(win)
    username_entry.pack()

    ttk.Label(win, text="Password").pack()
    password_entry = ttk.Entry(win, show="*")
    password_entry.pack()

    ttk.Label(win, text="Confirm Password").pack()
    confirm_entry = ttk.Entry(win, show="*")
    confirm_entry.pack()

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            win.destroy()
        except:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    ttk.Button(win, text="Register", command=register_user, bootstyle="success").pack(pady=10)
