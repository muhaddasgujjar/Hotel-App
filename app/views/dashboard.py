from ttkbootstrap import Window, Notebook, Frame, Label, Entry, Combobox, Button, Treeview
from ttkbootstrap.constants import *
from tkinter import Toplevel, messagebox
from app.models.database import get_connection

def open_dashboard(login_window, username):
    login_window.destroy()

    win = Window(themename="solar")
    win.title(f"Dashboard - Welcome {username}")
    win.geometry("950x620")
    win.resizable(False, False)

    Label(win, text=f"🏨 Hotel Dashboard - Welcome, {username}", font=("Segoe UI", 18, "bold"), bootstyle="info").pack(pady=15)

    notebook = Notebook(win, bootstyle="primary")
    notebook.pack(fill='both', expand=True, padx=20, pady=10)

    style_table = dict(columns=("ID", "Room", "Type", "Status"), show="headings", height=10)

    # TAB 1 - Add Room
    tab1 = Frame(notebook)
    notebook.add(tab1, text="➕ Add Room")

    Label(tab1, text="Room Number:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=20, pady=15, sticky='e')
    room_num_entry = Entry(tab1, width=30)
    room_num_entry.grid(row=0, column=1)

    Label(tab1, text="Room Type:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=20, pady=15, sticky='e')
    room_type_entry = Entry(tab1, width=30)
    room_type_entry.grid(row=1, column=1)

    def save_room():
        num, rtype = room_num_entry.get(), room_type_entry.get()
        if not num or not rtype:
            messagebox.showerror("Error", "All fields are required.")
            return
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO rooms (room_number, room_type, status) VALUES (?, ?, 'Available')", (num, rtype))
            conn.commit()
            messagebox.showinfo("Success", "Room added successfully!")
            room_num_entry.delete(0, 'end')
            room_type_entry.delete(0, 'end')
            load_rooms()
            load_available_rooms()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    Button(tab1, text="Add Room", bootstyle="success-outline", command=save_room).grid(row=2, column=1, pady=10)

    # TAB 2 - Available Rooms
    tab2 = Frame(notebook)
    notebook.add(tab2, text="✅ Available Rooms")

    avail_table = Treeview(tab2, **style_table)
    for col in style_table['columns']:
        avail_table.heading(col, text=col)
        avail_table.column(col, width=150)
    avail_table.pack(padx=10, pady=15)

    def load_available_rooms():
        for row in avail_table.get_children():
            avail_table.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rooms WHERE status='Available'")
        for row in cur.fetchall():
            avail_table.insert('', 'end', values=row)
        conn.close()

    # TAB 3 - View Rooms
    tab3 = Frame(notebook)
    notebook.add(tab3, text="📋 View Rooms")

    view_table = Treeview(tab3, **style_table)
    for col in style_table['columns']:
        view_table.heading(col, text=col)
        view_table.column(col, width=150)
    view_table.pack(padx=10, pady=15)

    def load_rooms():
        for row in view_table.get_children():
            view_table.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rooms")
        for row in cur.fetchall():
            view_table.insert('', 'end', values=row)
        conn.close()

    def delete_room():
        selected = view_table.selection()
        if not selected:
            messagebox.showerror("Error", "No room selected.")
            return
        room_id = view_table.item(selected[0])["values"][0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM rooms WHERE id=?", (room_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Room deleted successfully.")
        load_rooms()
        load_available_rooms()

    def update_room():
        selected = view_table.selection()
        if not selected:
            messagebox.showerror("Error", "No room selected.")
            return
        data = view_table.item(selected[0])["values"]
        popup = Toplevel(win)
        popup.geometry("400x300")
        popup.title("Update Room")

        Label(popup, text="Room Number:").pack(pady=5)
        room_num_upd = Entry(popup)
        room_num_upd.insert(0, data[1])
        room_num_upd.pack()

        Label(popup, text="Room Type:").pack(pady=5)
        room_type_upd = Entry(popup)
        room_type_upd.insert(0, data[2])
        room_type_upd.pack()

        Label(popup, text="Status:").pack(pady=5)
        status_upd = Combobox(popup, values=["Available Room", "Occupied"])
        status_upd.set(data[3])
        status_upd.pack()

        def save_update():
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE rooms SET room_number=?, room_type=?, status=? WHERE id=?",
                        (room_num_upd.get(), room_type_upd.get(), status_upd.get(), data[0]))
            conn.commit()
            conn.close()
            popup.destroy()
            load_rooms()
            load_available_rooms()
            messagebox.showinfo("Updated", "Room updated successfully.")

        Button(popup, text="Save", command=save_update, bootstyle="primary-outline").pack(pady=10)

    frame_btns = Frame(tab3)
    frame_btns.pack(pady=10)
    Button(frame_btns, text="Update", command=update_room, bootstyle="info").pack(side="left", padx=10)
    Button(frame_btns, text="Delete", command=delete_room, bootstyle="danger").pack(side="left", padx=10)

    # TAB 4 - Add Employee
    tab4 = Frame(notebook)
    notebook.add(tab4, text="👤 Add Employee")

    Label(tab4, text="Name of Employee:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=20, pady=15, sticky='e')
    emp_name = Entry(tab4, width=30)
    emp_name.grid(row=0, column=1)

    Label(tab4, text="Role of EMployee:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=20, pady=15, sticky='e')
    emp_role = Entry(tab4, width=30)
    emp_role.grid(row=1, column=1)

    def save_employee():
        name = emp_name.get()
        role = emp_role.get()
        if not name or not role:
            messagebox.showerror("Error", "All fields required.")
            return
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (name, role) VALUES (?, ?)", (name, role))
        conn.commit()
        conn.close()
        emp_name.delete(0, 'end')
        emp_role.delete(0, 'end')
        load_employees()
        messagebox.showinfo("Success", "Employee added.")

    Button(tab4, text="Add Employee", command=save_employee, bootstyle="success").grid(row=2, column=1, pady=10)

    # TAB 5 - View Employees
    tab5 = Frame(notebook)
    notebook.add(tab5, text="👥 View Employees")

    emp_table = Treeview(tab5, columns=("ID", "Name", "Role"), show="headings", height=10)
    for col in ("ID", "Name", "Role"):
        emp_table.heading(col, text=col)
        emp_table.column(col, width=160)
    emp_table.pack(pady=15)

    def load_employees():
        for row in emp_table.get_children():
            emp_table.delete(row)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        for row in cur.fetchall():
            emp_table.insert('', 'end', values=row)
        conn.close()

    # Initial load
    load_rooms()
    load_available_rooms()
    load_employees()

    win.mainloop()
# End of program