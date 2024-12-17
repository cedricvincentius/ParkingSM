import tkinter as tk
from tkinter import ttk

class ParkingGUI:
    def __init__(self, parking_system):
        self.parking_system = parking_system

        self.root = tk.Tk()
        self.root.title("Parking System Dashboard")

        self.table = ttk.Treeview(self.root, columns=("Vehicle", "Floor", "Fee"), show="headings")
        self.table.heading("Vehicle", text="Vehicle")
        self.table.heading("Floor", text="Floor")
        self.table.heading("Fee", text="Fee")
        self.table.pack(fill=tk.BOTH, expand=True)

    def update_table(self):
        records = self.parking_system.db.execute("SELECT * FROM parking_history WHERE date(start_time) = CURRENT_DATE")
        for record in records:
            self.table.insert("", "end", values=(record["vehicle_type"], record["floor"], record["fee"]))

    def run(self):
        self.update_table()
        self.root.mainloop()
