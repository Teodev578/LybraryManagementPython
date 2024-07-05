from pathlib import Path
import customtkinter as ctk
import mysql.connector
from tkinter import Canvas, messagebox, ttk
from Connexion import DatabaseConnection
from Observer import DatabaseObserver

class UserManagementWidget(ctk.CTkFrame):
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
        columns = ("id", "username", "password")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Password")

        # Place the tree on the canvas
        self.tree.place(x=28.0, y=418.0, width=1219.0, height=268.0)

        # Bind the selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create other UI elements as before
        self.create_ui_elements()

        # Set up the observer to update the TreeView
        self.observer = DatabaseObserver(self.db_connection, interval=10)
        self.observer.register_observer(self)
        self.observer.start(self.observer.fetch_data_users)

    def create_ui_elements(self):
        button_1 = ctk.CTkButton(master=self, text="Ajouter", width=250, height=50, command=self.add_user)
        button_1.place(x=144.0, y=705.0)

        button_2 = ctk.CTkButton(master=self, text="Modifier", width=250, height=50, command=self.modify_user)
        button_2.place(x=515.0, y=705.0)

        button_3 = ctk.CTkButton(master=self, text="Supprimer", width=250, height=50, command=self.delete_user)
        button_3.place(x=886.0, y=705.0)

        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#217FC4", outline="")
        self.canvas.create_text(28.0, 1.0, anchor="nw", text="Gestion utilisateurs", fill="#FFFFFF", font=("Inter Bold", 32 * -1))

        self.entry_1 = ctk.CTkEntry(master=self, width=280, height=33, fg_color="#313131", text_color="#FFFFFF")
        self.entry_1.place(x=38.0, y=140.0)

        self.entry_2 = ctk.CTkEntry(master=self, width=280, height=33, fg_color="#313131", text_color="#FFFFFF")
        self.entry_2.place(x=38.0, y=221.0)

        self.canvas.create_text(28.0, 111.0, anchor="nw", text="utilisateur", fill="#FFFFFF", font=("Inter Medium", 20 * -1))
        self.canvas.create_text(28.0, 192.0, anchor="nw", text="Mot de passe", fill="#FFFFFF", font=("Inter Medium", 20 * -1))

        self.search_entry = ctk.CTkEntry(master=self, width=537, height=33, fg_color="#313131", text_color="#FFFFFF")
        self.search_entry.place(x=390.0, y=140.0)
        self.search_entry.bind("<KeyRelease>", self.search_user)

        self.canvas.create_text(380.0, 111.0, anchor="nw", text="Recherche", fill="#FFFFFF", font=("Inter Medium", 20 * -1))

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            values = self.tree.item(selected_item, "values")
            self.entry_1.delete(0, "end")
            self.entry_1.insert(0, values[1])  # username
            self.entry_2.delete(0, "end")
            self.entry_2.insert(0, values[2])  # password
        else:
            # Si aucune sélection n'est faite, effacez les entrées
            self.entry_1.delete(0, "end")
            self.entry_2.delete(0, "end")

    def update(self, data):
        # Clear the current content of the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data into the treeview
        for row in data:
            self.tree.insert("", "end", values=row)


    def add_user(self):
        username = self.entry_1.get()
        password = self.entry_2.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty")
            return

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        params = (username, password)

        try:
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query, params)
            self.db_connection._connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "User added successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Clear the entry fields
        self.entry_1.delete(0, "end")
        self.entry_2.delete(0, "end")

        # Refresh the TreeView
        self.observer.check_for_updates(self.observer.fetch_data_users)

    def modify_user(self):
        selected_item = self.tree.selection()[0]
        user_id = self.tree.item(selected_item, "values")[0]
        username = self.entry_1.get()
        password = self.entry_2.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty")
            return

        query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
        params = (username, password, user_id)

        try:
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query, params)
            self.db_connection._connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "User updated successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Clear the entry fields
        self.entry_1.delete(0, "end")
        self.entry_2.delete(0, "end")

        # Refresh the TreeView
        self.observer.check_for_updates(self.observer.fetch_data_users)

    def delete_user(self):
        selected_item = self.tree.selection()[0]
        user_id = self.tree.item(selected_item, "values")[0]

        query = "DELETE FROM users WHERE id = %s"
        params = (user_id,)

        try:
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query, params)
            self.db_connection._connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "User deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Clear the entry fields
        self.entry_1.delete(0, "end")
        self.entry_2.delete(0, "end")

        # Refresh the TreeView
        self.observer.check_for_updates(self.observer.fetch_data_users)

    def search_user(self, event):
        search_term = self.search_entry.get().lower()
        data = self.fetch_all_users()

        filtered_data = [
            user for user in data
            if search_term in user[1].lower() or search_term in user[2].lower()
        ]

        self.update(filtered_data)

    def fetch_all_users(self):
        return self.observer.fetch_data_users()

# Example usage
if __name__ == "__main__":
    window = ctk.CTk()
    window.geometry("1280x773")
    window.configure(fg_color="#282828")
    user_management_widget = UserManagementWidget(window)
    user_management_widget.pack(fill="both", expand=True)
    window.mainloop()
