from pathlib import Path
import customtkinter as ctk
import mysql.connector
from tkinter import Canvas, messagebox, ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

from Connexion import DatabaseConnection
from Observer import DatabaseObserver


class BookManagementWidget(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#282828")
        self.db_connection = DatabaseConnection.get_instance(
            host="localhost",
            username="root",
            password="OKok__1325__",
            database="Lybrary"
        )

        self.db_observer = DatabaseObserver(self.db_connection)
        self.db_observer.register_observer(self)

        # Define the path to assets
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"/home/fabien/Documents/Projet/Projet Mida/Library pyhton project/build/assets/frame4")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
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
        columns = ("id", "title", "author", "isbn", "publisher", "year", "copies", "category")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Titre")
        self.tree.heading("author", text="Auteur")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("publisher", text="Éditeur")
        self.tree.heading("year", text="Année")
        self.tree.heading("copies", text="Exemplaires")
        self.tree.heading("category", text="Catégorie")
        
        # Define column widths
        self.tree.column("id", width=50)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("isbn", width=100)
        self.tree.column("publisher", width=150)
        self.tree.column("year", width=70)
        self.tree.column("copies", width=90)
        self.tree.column("category", width=120)

        # Place the tree on the canvas
        self.tree.place(x=28.0, y=418.0, width=1219.0, height=268.0)

        # Bind the selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create other UI elements
        self.create_ui_elements()

        self.load_books()

    def create_ui_elements(self):
        button_1 = ctk.CTkButton(
            master=self, text="Ajouter", width=250, height=50, command=self.add_book)
        button_1.place(x=144.0, y=705.0)

        button_2 = ctk.CTkButton(
            master=self,
            text="Modifier",
            width=250,
            height=50,
            command=self.modify_book
        )
        button_2.place(x=515.0, y=705.0)

        button_3 = ctk.CTkButton(
            master=self,
            text="Supprimer",
            width=250,
            height=50,
            command=self.delete_book
        )
        button_3.place(x=886.0, y=705.0)

        self.canvas.create_rectangle(
            0.0,
            0.0,
            1280.0,
            50.0,
            fill="#217FC4",
            outline=""
        )

        self.canvas.create_text(
            28.0,
            1.0,
            anchor="nw",
            text="Gestion des livres",
            fill="#FFFFFF",
            font=("Inter Bold", 32 * -1)
        )

        self.entries = {}
        
        # Labels for the entries
        self.canvas.create_text(
            38.0, 80.0,
            anchor="nw",
            text="Titre:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
            358.0, 80.0,
            anchor="nw",
            text="Auteur:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
             678.0, 80.0,
            anchor="nw",
            text="ISBN:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
             38.0, 160.0,
            anchor="nw",
            text="Éditeur:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
             358.0, 160.0,
            anchor="nw",
            text="Année:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
             678.0, 160.0,
            anchor="nw",
            text="Exemplaires:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
             358.0, 243.0,
            anchor="nw",
            text="Catégorie:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )
        self.canvas.create_text(
             38.0, 310.0,
            anchor="nw",
            text="Description:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )

        self.entries['title'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['title'].place(x=38.0, y=98.0)
        
        self.entries['author'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['author'].place(x=358.0, y=98.0)
        
        self.entries['isbn'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['isbn'].place(x=678.0, y=98.0)

        self.entries['publisher'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['publisher'].place(x=38.0, y=180.0)
        
        self.entries['year'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['year'].place(x=358.0, y=180.0)
        
        self.entries['copies'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['copies'].place(x=678.0, y=180.0)
        
        self.entries['category'] = ctk.CTkComboBox(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['category'].place(x=358.0, y=263.0)
        self.load_categories()  # Load categories into the combobox
        
        self.entries['description'] = ctk.CTkTextbox(
            master=self,
            width=620,
            height=70,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['description'].place(x=38.0, y=330.0)
        
        self.select_image_button = ctk.CTkButton(
            master=self,
            text="Sélectionner une image",
            width=250,
            height=50,
            command=self.select_image
        )
        self.select_image_button.place(x=1010.0, y=320.0)

        self.cover_label = ctk.CTkLabel(self, text="", width=186.0, height=220.0)
        self.cover_label.place(x=1010.0, y=100.0)
        
        # Search Entry
        self.canvas.create_text(
            678.0, 243.0,
            anchor="nw",
            text="Recherche:",
            fill="#FFFFFF",
            font=("Inter Regular", 14)
        )

        self.entries['search'] = ctk.CTkEntry(
            master=self,
            width=280,
            height=33,
            fg_color="#313131",
            text_color="#FFFFFF"
        )
        self.entries['search'].place(x=678.0, y=263.0)
        self.entries['search'].bind("<KeyRelease>", self.filter_books)

    def load_categories(self):
        query = "SELECT categorie FROM Categories"
        categories = self.db_connection.execute_query(query)
        category_names = [category[0] for category in categories]
        self.entries['category'].configure(values=category_names)
    
    def load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        query = "SELECT id, title, author, isbn, publisher, years, copies, category FROM Livre"
        books = self.db_connection.execute_query(query)
        
        for book in books:
            self.tree.insert("", ctk.END, values=book)

    def filter_books(self, event):
        search_term = self.entries['search'].get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        query = "SELECT id, title, author, isbn, publisher, years, copies, category FROM Livre"
        books = self.db_connection.execute_query(query)
        
        for book in books:
            if any(search_term in str(field).lower() for field in book):
                self.tree.insert("", ctk.END, values=book)

    def on_tree_select(self, event):
        selection = self.tree.selection()
        if selection:
            book_id = self.tree.item(selection[0], "values")[0]
            self.load_book_details(book_id)

    def load_book_details(self, book_id):
        query = "SELECT title, author, isbn, publisher, years, copies, descriptions, category, cover FROM Livre WHERE id = %s"
        book_details = self.db_connection.execute_query(query, (book_id,))
        if book_details:
            book = book_details[0]
            self.entries['title'].delete(0, ctk.END)
            self.entries['title'].insert(0, book[0])
            self.entries['author'].delete(0, ctk.END)
            self.entries['author'].insert(0, book[1])
            self.entries['isbn'].delete(0, ctk.END)
            self.entries['isbn'].insert(0, book[2])
            self.entries['publisher'].delete(0, ctk.END)
            self.entries['publisher'].insert(0, book[3])
            self.entries['year'].delete(0, ctk.END)
            self.entries['year'].insert(0, book[4])
            self.entries['copies'].delete(0, ctk.END)
            self.entries['copies'].insert(0, book[5])
            self.entries['description'].delete('1.0', ctk.END)
            self.entries['description'].insert('1.0', book[6])
            self.entries['category'].set(book[7])  # Set the selected category in the combobox
            if book[8]:
                self.display_image(book[8])

        self.cover_image_path = ""  # Variable pour stocker le chemin de l'image de couverture

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.cover_image_path = file_path
            self.display_image(file_path)
    
    def display_image(self, file_path):
        self.cover_image = Image.open(file_path)
        self.cover_image.thumbnail((186, 220))
        img = ImageTk.PhotoImage(self.cover_image)
        self.cover_label.configure(image=img)
        self.cover_label.image = img

    def add_book(self):
        title = self.entries['title'].get()
        author = self.entries['author'].get()
        isbn = self.entries['isbn'].get()
        publisher = self.entries['publisher'].get()
        year = self.entries['year'].get()
        copies = self.entries['copies'].get()
        description = self.entries['description'].get('1.0', ctk.END)
        category = self.entries['category'].get()  # Get the selected category
        cover = self.cover_image_path

        if not title or not author or not isbn:
            messagebox.showwarning("Input Error", "Title, author, and ISBN cannot be empty")
            return

        query = "INSERT INTO Livre (title, author, isbn, publisher, years, copies, descriptions, category, cover) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (title, author, isbn, publisher, year, copies, description, category, cover)

        try:
            self.db_connection.execute_query(query, params)
            messagebox.showinfo("Success", "Book added successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Refresh the TreeView
        self.load_books()

    def modify_book(self):
        selected_item = self.tree.selection()[0]
        book_id = self.tree.item(selected_item, "values")[0]
        title = self.entries['title'].get()
        author = self.entries['author'].get()
        isbn = self.entries['isbn'].get()
        publisher = self.entries['publisher'].get()
        year = self.entries['year'].get()
        copies = self.entries['copies'].get()
        description = self.entries['description'].get('1.0', ctk.END)
        category = self.entries['category'].get()  # Get the selected category
        cover = self.cover_image_path

        if not title or not author or not isbn:
            messagebox.showwarning("Input Error", "Title, author, and ISBN cannot be empty")
            return

        query = "UPDATE Livre SET title = %s, author = %s, isbn = %s, publisher = %s, years = %s, copies = %s, descriptions = %s, category = %s, cover = %s WHERE id = %s"
        params = (title, author, isbn, publisher, year, copies, description, category, cover, book_id)

        try:
            self.db_connection.execute_query(query, params)
            messagebox.showinfo("Success", "Book updated successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Refresh the TreeView
        self.load_books()

    def delete_book(self):
        selected_item = self.tree.selection()[0]
        book_id = self.tree.item(selected_item, "values")[0]

        query = "DELETE FROM Livre WHERE id = %s"
        params = (book_id,)

        try:
            self.db_connection.execute_query(query, params)
            messagebox.showinfo("Success", "Book deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Refresh the TreeView
        self.load_books()

    def update(self, data):
        self.load_books()

# Example usage
if __name__ == "__main__":
    window = ctk.CTk()
    window.geometry("1280x773")
    window.configure(fg_color="#282828")  # Use fg_color instead of bg
    book_management_widget = BookManagementWidget(window)
    book_management_widget.pack(fill="both", expand=True)
    window.mainloop()
