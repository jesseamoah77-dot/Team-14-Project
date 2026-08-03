"""
dashboard.py
GridCare-Lite - Outage Dashboard

Shows a table of all reported outages (joined with substation name and
region so it's readable). Engineers and admins can log a new outage.
Admins can also assign work orders to technicians.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from database import init_db


class OutageDashboard(tk.Frame):
    def __init__(self, master, user_id, username, role, db_path='gridcare.db'):
        super().__init__(master)
        self.user_id = user_id
        self.username = username
        self.role = role
        self.db_path = db_path
        self.master = master
        master.title(f'GridCare-Lite - Outage Dashboard ({username} - {role})')

        columns = ('outage_id', 'substation', 'region', 'description', 'status', 'reported_at')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=12)
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=120)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text='Refresh', command=self.load_outages).pack(
            side='left', padx=5
        )

        # Only engineers and admins can log a new outage
        if role in ('engineer', 'admin'):
            ttk.Button(
                button_frame, text='Log New Outage', command=self.open_new_outage_form
            ).pack(side='left', padx=5)

        # Only admins can assign work orders
        if role == 'admin':
            ttk.Button(
                button_frame, text='Assign Work Order', command=self.open_assign_form
            ).pack(side='left', padx=5)

        self.pack(fill='both', expand=True)
        self.load_outages()

    def load_outages(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = init_db(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            SELECT o.outage_id, s.name, s.region, o.description, o.status, o.reported_at
            FROM outages o
            JOIN substations s ON o.substation_id = s.substation_id
            ORDER BY o.reported_at DESC
        ''')
        for row in cur.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()

    def open_new_outage_form(self):
        NewOutageForm(self, self.user_id, on_submit=self.load_outages, db_path=self.db_path)

    def open_assign_form(self):
        AssignWorkOrderForm(self, on_submit=self.load_outages, db_path=self.db_path)


class NewOutageForm(tk.Toplevel):
    def __init__(self, parent, reported_by_user_id, on_submit, db_path='gridcare.db'):
        super().__init__(parent)
        self.title('Log New Outage')
        self.reported_by_user_id = reported_by_user_id
        self.on_submit = on_submit
        self.db_path = db_path

        conn = init_db(db_path)
        cur = conn.cursor()
        cur.execute('SELECT substation_id, name FROM substations ORDER BY name')
        self.substations = cur.fetchall()
        conn.close()

        ttk.Label(self, text='Substation:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        self.substation_var = tk.StringVar()
        substation_names = [name for _, name in self.substations]
        self.substation_combo = ttk.Combobox(
            self, textvariable=self.substation_var, values=substation_names, state='readonly'
        )
        self.substation_combo.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(self, text='Description:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.description_entry = ttk.Entry(self, width=30)
        self.description_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Button(self, text='Submit', command=self.submit).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def submit(self):
        selected_name = self.substation_var.get()
        description = self.description_entry.get().strip()

        if not selected_name or not description:
            messagebox.showerror('Missing Info', 'Please select a substation and enter a description.')
            return

        substation_id = next(
            sub_id for sub_id, name in self.substations if name == selected_name
        )

        conn = init_db(self.db_path)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO outages (substation_id, reported_by, description) VALUES (?, ?, ?)',
            (substation_id, self.reported_by_user_id, description)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo('Success', 'Outage logged successfully.')
        self.on_submit()
        self.destroy()


class AssignWorkOrderForm(tk.Toplevel):
    """
    Lets an admin pick an open outage, assign a technician, and set a
    scheduled date. Creates a work order and bumps the outage's status
    to 'In Progress'.
    """

    def __init__(self, parent, on_submit, db_path='gridcare.db'):
        super().__init__(parent)
        self.title('Assign Work Order')
        self.on_submit = on_submit
        self.db_path = db_path

        conn = init_db(db_path)
        cur = conn.cursor()

        cur.execute('''
            SELECT o.outage_id, s.name, o.description
            FROM outages o
            JOIN substations s ON o.substation_id = s.substation_id
            WHERE o.status = 'Open'
        ''')
        self.open_outages = cur.fetchall()

        cur.execute("SELECT user_id, username FROM users WHERE role = 'technician'")
        self.technicians = cur.fetchall()
        conn.close()

        outage_labels = [f"#{oid} - {name} - {desc}" for oid, name, desc in self.open_outages]
        tech_names = [name for _, name in self.technicians]

        ttk.Label(self, text='Open Outage:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        self.outage_var = tk.StringVar()
        self.outage_combo = ttk.Combobox(
            self, textvariable=self.outage_var, values=outage_labels, state='readonly', width=40
        )
        self.outage_combo.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(self, text='Assign Technician:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.tech_var = tk.StringVar()
        self.tech_combo = ttk.Combobox(
            self, textvariable=self.tech_var, values=tech_names, state='readonly'
        )
        self.tech_combo.grid(row=1, column=1, padx=8, pady=8)

        ttk.Label(self, text='Scheduled Date (YYYY-MM-DD):').grid(
            row=2, column=0, padx=8, pady=8, sticky='e'
        )
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=8, pady=8)

        ttk.Button(self, text='Assign', command=self.submit).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    def submit(self):
        outage_label = self.outage_var.get()
        tech_name = self.tech_var.get()
        scheduled_date = self.date_entry.get().strip()

        if not outage_label or not tech_name or not scheduled_date:
            messagebox.showerror('Missing Info', 'Please fill in all fields.')
            return

        outage_id = int(outage_label.split(' - ')[0].replace('#', ''))
        tech_id = next(uid for uid, name in self.technicians if name == tech_name)

        conn = init_db(self.db_path)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO work_orders (outage_id, assigned_technician, scheduled_date, status) '
            'VALUES (?, ?, ?, ?)',
            (outage_id, tech_id, scheduled_date, 'Scheduled')
        )
        cur.execute(
            "UPDATE outages SET status = 'In Progress' WHERE outage_id = ?",
            (outage_id,)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo('Success', 'Work order created and technician assigned.')
        self.on_submit()
        self.destroy()
