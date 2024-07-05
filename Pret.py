import datetime
from tkinter import Canvas, Scrollbar, messagebox
from tkinter.ttk import Treeview, Combobox
from tkcalendar import DateEntry
from Observer import DatabaseObserver
from Connexion import DatabaseConnection
import customtkinter as ctk
from datetime import datetime


class LoanManagementWidget(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color="#282828")

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

        self.create_widgets()
        self.setup_database()
        self.load_data()

        # Set up the observer to update the TreeView
        self.observer = DatabaseObserver(self.db_connection, interval=60)
        self.observer.register_observer(self)
        self.observer.start(self.observer.fetch_data_loans)

    def create_widgets(self):
        # Create GUI components
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#217FC4", outline="")
        self.canvas.create_text(32.0, 0.0, anchor="nw", text="Gestion des Prêts", fill="#FFFFFF", font=("Inter Bold", 32 * -1))

        self.entry_membre_id = Combobox(self, width=27, height=33)
        self.entry_membre_id.place(x=38.0, y=98.0)

        self.entry_livre_id = Combobox(self, width=27, height=33)
        self.entry_livre_id.place(x=38.0, y=179.0)

        self.entry_date_debut = DateEntry(self, date_pattern="yyyy-mm-dd", background="darkblue", foreground="white", borderwidth=2, width=28, height=33)
        self.entry_date_debut.place(x=38.0, y=260.0)

        self.entry_date_fin = DateEntry(self, date_pattern="yyyy-mm-dd", background="darkblue", foreground="white", borderwidth=2, width=28, height=33)
        self.entry_date_fin.place(x=38.0, y=341.0)

        self.entry_recherche = ctk.CTkEntry(self, placeholder_text="Recherche", fg_color="#313131", width=537, height=33)
        self.entry_recherche.place(x=404.0, y=98.0)
        self.entry_recherche.bind("<KeyRelease>", self.rechercher_pret)

        self.create_labels()
        self.create_buttons()
        self.create_listview()

    def setup_database(self):
        # Initialize database connection
        try:
            self.db_connection = DatabaseConnection.get_instance(
                host="localhost",
                username="root",
                password="OKok__1325__",
                database="Lybrary"
            )
            self.load_comboboxes()
        except Exception as e:
            messagebox.showerror("Erreur de Connexion", f"Erreur lors de la connexion à la base de données : {e}")

    def load_comboboxes(self):
        # Load data into comboboxes
        try:
            membres = self.db_connection.execute_query("SELECT id, nom, prenom FROM Membres;")
            categories = self.db_connection.execute_query("SELECT id, title FROM Livre;")

            self.entry_membre_id['values'] = [f"{m[0]} - {m[1]} {m[2]}" for m in membres]
            self.entry_livre_id['values'] = [f"{c[0]} - {c[1]}" for c in categories]

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données: {e}")

    def create_labels(self):
        # Create labels on Canvas
        labels = [
            (28.0, 69.0, "ID Membre"),
            (28.0, 150.0, "ID Livre"),
            (28.0, 231.0, "Date de d'emprunt"),
            (28.0, 312.0, "Date de retour prévu"),
            #(394.0, 69.0, "Recherche"),
        ]
        for x, y, text in labels:
            self.canvas.create_text(x, y, anchor="nw", text=text, fill="#FFFFFF", font=("Inter Medium", 20 * -1))

    def create_buttons(self):
        # Create buttons
        buttons = [
            ("Ajouter", self.ajouter_pret, 144.0, 705.0),
            ("Modifier", self.modifier_pret, 515.0, 705.0),
            ("Supprimer", self.supprimer_pret, 886.0, 705.0),
        ]
        for text, command, x, y in buttons:
            button = ctk.CTkButton(self, text=text, command=command, width=250, height=50)
            button.place(x=x, y=y)

    def create_listview(self):
        # Create Treeview and Scrollbar
        self.listview = Treeview(self, columns=["ID", "ID Membre", "ID Livre", "Date de début", "Date de fin"], show="headings")
        self.listview.place(x=28.0, y=418.0, width=1219.0, height=268.0)
        for col in ["ID", "ID Membre", "ID Livre", "Date de début", "Date de fin"]:
            self.listview.heading(col, text=col)

        scrollbar = Scrollbar(self, orient="vertical", command=self.listview.yview)
        scrollbar.place(x=1247.0, y=418.0, height=268.0)
        self.listview.config(yscrollcommand=scrollbar.set)
        self.listview.bind("<<TreeviewSelect>>", self.on_item_selected)

    def load_data(self):
        # Load data from database
        try:
            data = self.db_connection.execute_query("SELECT * FROM Prets;")
            self.update_listview(data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des données: {e}")

    def update_listview(self, data):
        # Update Treeview with new data
        self.listview.delete(*self.listview.get_children())
        for row in data:
            self.listview.insert("", "end", values=row)

    def on_item_selected(self, event):
        # Handle Treeview item selection
        selected_item = self.listview.selection()
        if selected_item:
            item_values = self.listview.item(selected_item, "values")
            if item_values:
                self.entry_membre_id.set(f"{item_values[1]} - {self.get_member_name(item_values[1])}")
                self.entry_livre_id.set(f"{item_values[2]} - {self.get_category_name(item_values[2])}")
                self.entry_date_debut.set_date(item_values[3])
                self.entry_date_fin.set_date(item_values[4])

    def get_member_name(self, membre_id):
        try:
            result = self.db_connection.execute_query("SELECT nom, prenom FROM Membres WHERE id = %s", (membre_id,))
            if result:
                return f"{result[0][0]} {result[0][1]}"
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération du nom du membre: {e}")
        return ""

    def get_category_name(self, categorie_id):
        try:
            result = self.db_connection.execute_query("SELECT categorie FROM Categories WHERE id = %s", (categorie_id,))
            if result:
                return result[0][0]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération de la catégorie: {e}")
        return ""

    def ajouter_pret(self):
        membre_id = self.entry_membre_id.get().split(" - ")[0]
        livre_id = self.entry_livre_id.get().split(" - ")[0]
        date_debut = self.entry_date_debut.get()
        date_fin = self.entry_date_fin.get()

        # Convertir les dates en chaînes de caractères
        try:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d').strftime('%Y-%m-%d')
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError as e:
            messagebox.showerror("Erreur", f"Format de date invalide: {e}")
            return

        if membre_id and livre_id and date_debut and date_fin:
            try:
                query = "INSERT INTO Prets (membre_id, livre_id, date_debut, date_fin) VALUES (%s, %s, %s, %s)"
                rows_affected = self.db_connection.execute_query(query, (membre_id, livre_id, date_debut, date_fin))
                
                if rows_affected > 0:
                    messagebox.showinfo("Information", "Prêt ajouté avec succès.")
                    self.load_data()  # Mettre à jour la Treeview après l'ajout du prêt
                else:
                    messagebox.showerror("Erreur", "Aucun prêt n'a été ajouté.")
            except Exception as e:
                error_message = f"Erreur lors de l'ajout du prêt: {e}"
                print(error_message)  # Vous pouvez également écrire dans un fichier de log
                messagebox.showerror("Erreur", error_message)
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs nécessaires.")

    def modifier_pret(self):
        selected_item = self.listview.selection()
        if selected_item:
            membre_id = self.entry_membre_id.get().split(" - ")[0]
            livre_id = self.entry_livre_id.get().split(" - ")[0]
            date_debut = self.entry_date_debut.get()
            date_fin = self.entry_date_fin.get()

            if membre_id and livre_id and date_debut and date_fin:
                try:
                    item_values = self.listview.item(selected_item, "values")
                    pret_id = item_values[0]
                    query = "UPDATE Prets SET membre_id = %s, livre_id = %s, date_debut = %s, date_fin = %s WHERE id = %s"
                    self.db_connection.execute_query(query, (membre_id, livre_id, date_debut, date_fin, pret_id))
                    messagebox.showinfo("Information", "Le prêt a été modifié avec succès.")
                    self.load_data()  # Mettre à jour la Treeview après la modification du prêt
                except Exception as e:
                    error_message = f"Erreur lors de la modification du prêt: {e}"
                    print(error_message)  # Vous pouvez également écrire dans un fichier de log
                    messagebox.showerror("Erreur", error_message)
            else:
                messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs nécessaires.")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un prêt à modifier.")

    def supprimer_pret(self):
        # Delete loan from database
        selected_item = self.listview.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce prêt ?")
            if confirmation:
                try:
                    item_values = self.listview.item(selected_item, "values")
                    pret_id = item_values[0]
                    query = "DELETE FROM Prets WHERE id = %s"
                    self.db_connection.execute_query(query, (pret_id,))
                    messagebox.showinfo("Information", "Le prêt a été supprimé avec succès.")
                    self.observer.check_for_updates_loans()  # Notify observers
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la suppression du prêt: {e}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un prêt.")

    def rechercher_pret(self, event=None):
        # Search for loan in database
        recherche = self.entry_recherche.get()
        query = "SELECT * FROM Prets WHERE membre_id LIKE %s OR livre_id LIKE %s OR date_debut LIKE %s OR date_fin LIKE %s"
        try:
            data = self.db_connection.execute_query(query, (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%"))
            self.update_listview(data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche de prêts: {e}")

    def update(self, data):
        # Observer update method to refresh data in Treeview
        self.update_listview(data)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1280x773")
    widget = LoanManagementWidget(root)
    widget.pack(fill="both", expand=True)
    root.resizable(False, False)
    root.mainloop()
