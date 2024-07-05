from pathlib import Path
import customtkinter as ctk
import mysql.connector
from tkinter import Canvas, messagebox, ttk, filedialog
from Connexion import DatabaseConnection
from Observer import DatabaseObserver


class CategoryManagementWidget(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#282828")
        self.db_connection = DatabaseConnection.get_instance(
            host="localhost",
            username="root",
            password="OKok__1325__",
            database="Lybrary"
        )

        # Create a canvas
        self.canvas = Canvas(
            self,
            bg="#282828",
            height=773,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create a ListView using Treeview from ttk
        columns = ("id", "categorie")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("categorie", text="Category Name")

        # Place the tree on the canvas
        self.tree.place(x=28.0, y=418.0, width=1219.0, height=268.0)

        # Bind the selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create other UI elements as before
        self.create_ui_elements()

        # Set up the observer to update the TreeView
        self.observer = DatabaseObserver(self.db_connection, interval=20)
        self.observer.register_observer(self)
        self.observer.start(self.observer.fetch_data_categories)

    def create_ui_elements(self):
        button_1 = ctk.CTkButton(master=self, text="Ajouter", width=250, height=50, command=self.add_category)
        button_1.place(x=144.0, y=705.0)

        button_2 = ctk.CTkButton(master=self, text="Modifier", width=250, height=50, command=self.modify_category)
        button_2.place(x=515.0, y=705.0)

        button_3 = ctk.CTkButton(master=self, text="Supprimer", width=250, height=50, command=self.delete_category)
        button_3.place(x=886.0, y=705.0)

        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#217FC4", outline="")
        self.canvas.create_text(28.0, 1.0, anchor="nw", text="Gestion des catégories", fill="#FFFFFF", font=("Inter Bold", 32 * -1))

        self.entry_1 = ctk.CTkEntry(master=self, width=280, height=33, fg_color="#313131", text_color="#FFFFFF")
        self.entry_1.place(x=38.0, y=140.0)

        self.canvas.create_text(28.0, 111.0, anchor="nw", text="Nom de la catégorie", fill="#FFFFFF", font=("Inter Medium", 20 * -1))

        self.search_entry = ctk.CTkEntry(master=self, width=537, height=33, fg_color="#313131", text_color="#FFFFFF")
        self.search_entry.place(x=390.0, y=140.0)
        self.search_entry.bind("<KeyRelease>", self.search_category)

        self.canvas.create_text(380.0, 111.0, anchor="nw", text="Recherche", fill="#FFFFFF", font=("Inter Medium", 20 * -1))

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            values = self.tree.item(selected_item, "values")
            self.entry_1.delete(0, "end")
            self.entry_1.insert(0, values[1])  # categorie
        else:
            # Si aucune sélection n'est faite, effacez les entrées
            self.entry_1.delete(0, "end")

    def update(self, data):
        # Schedule the update to be run in the main thread
        self.after(0, self.update_ui, data)

    def update_ui(self, data):
        current_data = [self.tree.item(item, "values") for item in self.tree.get_children()]
        if current_data != data:
            # Clear the current content of the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data into the treeview
            for row in data:
                self.tree.insert("", "end", values=row)

    def add_category(self):
        category_name = self.entry_1.get()

        if not category_name:
            messagebox.showwarning("Input Error", "Category name cannot be empty")
            return

        query = "INSERT INTO Categories (categorie) VALUES (%s)"
        params = (category_name,)

        try:
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query, params)
            self.db_connection._connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Category added successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Clear the entry fields
        self.entry_1.delete(0, "end")

        # Refresh the TreeView
        self.observer.check_for_updates(self.observer.fetch_data_categories)

    def modify_category(self):
        selected_item = self.tree.selection()[0]
        category_id = self.tree.item(selected_item, "values")[0]
        category_name = self.entry_1.get()

        if not category_name:
            messagebox.showwarning("Input Error", "Category name cannot be empty")
            return

        query = "UPDATE Categories SET categorie = %s WHERE id = %s"
        params = (category_name, category_id)

        try:
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query, params)
            self.db_connection._connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Category updated successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Clear the entry fields
        self.entry_1.delete(0, "end")

        # Refresh the TreeView
        self.observer.check_for_updates(self.observer.fetch_data_categories)

    def delete_category(self):
        selected_item = self.tree.selection()[0]
        category_id = self.tree.item(selected_item, "values")[0]

        query = "DELETE FROM Categories WHERE id = %s"
        params = (category_id,)

        try:
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query, params)
            self.db_connection._connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Category deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Clear the entry fields
        self.entry_1.delete(0, "end")

        # Refresh the TreeView
        self.observer.check_for_updates(self.observer.fetch_data_categories)

    def search_category(self, event):
        search_term = self.search_entry.get().lower()
        data = self.fetch_all_categories()

        filtered_data = [
            category for category in data
            if search_term in category[1].lower()
        ]

        self.update(filtered_data)

    def fetch_all_categories(self):
        return self.observer.fetch_data_categories()


# Example usage
if __name__ == "__main__":
    window = ctk.CTk()
    window.geometry("1280x773")
    window.configure(fg_color="#282828")
    category_management_widget = CategoryManagementWidget(window)
    category_management_widget.pack(fill="both", expand=True)
    window.mainloop()
