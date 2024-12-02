import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import folium
import webbrowser
import difflib


class MosqueManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Mosques Management System")

        # Initialize SQLite database connection
        self.conn = sqlite3.connect('data_entries.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

        # Initialize UI Components
        self.create_ui()
        self.refresh_treeview()

    def setup_database(self):
        """Set up the SQLite database."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            type TEXT,
            coordinates TEXT,
            name TEXT,
            address TEXT,
            imam_name TEXT
        )
        """)
        self.conn.commit()

    def create_ui(self):
        """Create the UI components."""
        # Input Fields
        Label(self.root, text='ID').grid(row=1, column=1, padx=5, pady=5)
        Label(self.root, text='Type').grid(row=2, column=1, padx=5, pady=5)
        Label(self.root, text='Coordinates').grid(row=3, column=1, padx=5, pady=5)

        self.id_entry = Entry(self.root)
        self.id_entry.grid(row=1, column=2, padx=5, pady=5)

        self.type_var = StringVar(value="Option 1")
        OptionMenu(self.root, self.type_var, "Option 1", "Option 2", "Option 3").grid(row=2, column=2, padx=5, pady=5)

        self.coordinates_entry = Entry(self.root)
        self.coordinates_entry.grid(row=3, column=2, padx=5, pady=5)

        Label(self.root, text='Name').grid(row=1, column=3, padx=5, pady=5)
        Label(self.root, text='Address').grid(row=2, column=3, padx=5, pady=5)
        Label(self.root, text='Imam Name').grid(row=3, column=3, padx=5, pady=5)

        self.name_entry = Entry(self.root)
        self.name_entry.grid(row=1, column=4, padx=5, pady=5)

        self.address_entry = Entry(self.root)
        self.address_entry.grid(row=2, column=4, padx=5, pady=5)

        self.imam_name_entry = Entry(self.root)
        self.imam_name_entry.grid(row=3, column=4, padx=5, pady=5)

        # Buttons
        Button(self.root, text="Add Entry", command=self.add_entry).grid(row=4, column=2, padx=5, pady=5)
        Button(self.root, text="Update Entry", command=self.update_entry).grid(row=4, column=3, padx=5, pady=5)
        Button(self.root, text="Delete Entry", command=self.delete_entry).grid(row=4, column=4, padx=5, pady=5)
        Button(self.root, text="Display All", command=self.display_all).grid(row=5, column=2, padx=5, pady=5)
        Button(self.root, text="Search By Imam Name", command=self.search_by_imam_name).grid(row=5, column=3, padx=5, pady=5)
        Button(self.root, text="Display on Map", command=self.display_on_map).grid(row=5, column=4, padx=5, pady=5)

        # Treeview for Data Display
        frame = Frame(self.root)
        frame.grid(row=1, column=5, rowspan=5, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(frame, columns=("ID", "Type", "Coordinates", "Name", "Address", "Imam Name"), show='headings')
        for col in ("ID", "Type", "Coordinates", "Name", "Address", "Imam Name"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=CENTER)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def add_entry(self):
        values = (
            self.id_entry.get(),
            self.type_var.get(),
            self.coordinates_entry.get(),
            self.name_entry.get(),
            self.address_entry.get(),
            self.imam_name_entry.get(),
        )
        if not all(values):
            messagebox.showerror("Error", "All fields are required!")
            return
        self.cursor.execute("INSERT INTO entries (id, type, coordinates, name, address, imam_name) VALUES (?, ?, ?, ?, ?, ?)", values)
        self.conn.commit()
        self.refresh_treeview()
        self.clear_entries()

    def update_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an entry to update!")
            return
        selected_id = self.tree.item(selected_item)["values"][0]
        updated_values = (
            self.type_var.get(),
            self.coordinates_entry.get(),
            self.name_entry.get(),
            self.address_entry.get(),
            self.imam_name_entry.get(),
            selected_id
        )
        self.cursor.execute("""
        UPDATE entries SET type = ?, coordinates = ?, name = ?, address = ?, imam_name = ? WHERE id = ?
        """, updated_values)
        self.conn.commit()
        self.refresh_treeview()
        self.clear_entries()

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an entry to delete!")
            return
        selected_id = self.tree.item(selected_item)["values"][0]
        self.cursor.execute("DELETE FROM entries WHERE id = ?", (selected_id,))
        self.conn.commit()
        self.refresh_treeview()

    def display_all(self):
        self.tree.delete(*self.tree.get_children()) ## to clear the tree view ... to avoid dublicate 
        self.cursor.execute("SELECT * FROM entries")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", END, values=row)

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM entries")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", END, values=row)


    def search_by_imam_name(self):
        imam_name = self.imam_name_entry.get()
        if not imam_name:
            messagebox.showerror("Error", "Imam Name field is empty!")
            return

        
        self.cursor.execute("SELECT imam_name FROM entries")
        all_imam_names = [row[0] for row in self.cursor.fetchall()]

        # Find exact matches
        self.cursor.execute("SELECT * FROM entries WHERE imam_name = ?", (imam_name,))
        rows = self.cursor.fetchall()

        if rows:
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", END, values=row)
        else:
            # No exact match found sugges.... to cloxe one
            close_matches = difflib.get_close_matches(imam_name, all_imam_names, n=5, cutoff=0.6)
            if close_matches:
                suggested_names = "\n".join(close_matches)
                selected_name = messagebox.askquestion(
                    "Not Found",
                    f"No exact match found for '{imam_name}'.\nDid you mean:\n\n{suggested_names}\n\n?"
                )
                if selected_name == "yes":
                    
                    self.cursor.execute("SELECT * FROM entries WHERE imam_name = ?", (close_matches[0],))
                    rows = self.cursor.fetchall()
                    self.tree.delete(*self.tree.get_children())
                    for row in rows:
                        self.tree.insert("", END, values=row)
            else:
                
                messagebox.showinfo("Not Found", f"No entry found with Imam Name '{imam_name}' and no close matches.")
            

    def display_on_map(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an entry to display on map!")
            return
        coordinates = self.tree.item(selected_item)["values"][2]
        name = self.tree.item(selected_item)["values"][3]
        try:
            lat, lon = map(float, coordinates.split(","))
            map_obj = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup=name).add_to(map_obj)
            map_obj.save("map.html")
            webbrowser.open("map.html")
        except ValueError:
            messagebox.showerror("Error", "Invalid coordinates format! Use 'latitude,longitude'.")

    def clear_entries(self):
        """Clear all input fields."""
        self.id_entry.delete(0, END)
        self.type_var.set("Option 1")
        self.coordinates_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.imam_name_entry.delete(0, END)


# Test 
if __name__ == "__main__":
    root = Tk()
    app = MosqueManagementSystem(root)
    root.mainloop()
