import datetime
from tkinter import Canvas, Scrollbar, messagebox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from Observer import DatabaseObserver
from Connexion import DatabaseConnection
import customtkinter as ctk
from datetime import datetime


class MemberManagementWidget(ctk.CTkFrame):
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
        self.observer.start(self.observer.fetch_data_members)

    def create_widgets(self):
        # Create GUI components
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#217FC4", outline="")
        self.canvas.create_text(32.0, 0.0, anchor="nw", text="Gestion des Membres", fill="#FFFFFF", font=("Inter Bold", 32 * -1))

        self.entry_nom = ctk.CTkEntry(self, placeholder_text="Nom", fg_color="#313131", width=280, height=33)
        self.entry_nom.place(x=38.0, y=98.0)

        self.entry_prenom = ctk.CTkEntry(self, placeholder_text="Prénom", fg_color="#313131", width=280, height=33)
        self.entry_prenom.place(x=38.0, y=179.0)

        self.entry_telephone = ctk.CTkEntry(self, placeholder_text="Numéro de téléphone", fg_color="#313131", width=280, height=33)
        self.entry_telephone.place(x=38.0, y=260.0)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email", fg_color="#313131", width=280, height=33)
        self.entry_email.place(x=38.0, y=341.0)

        self.entry_recherche = ctk.CTkEntry(self, placeholder_text="Recherche", fg_color="#313131", width=537, height=33)
        self.entry_recherche.place(x=404.0, y=98.0)
        self.entry_recherche.bind("<KeyRelease>", self.rechercher_membre)

        self.entry_date = DateEntry(self, date_pattern="yyyy-mm-dd", background="darkblue", foreground="white", borderwidth=2, width=28, height=33)
        self.entry_date.place(x=404.0, y=179.0)

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
        except Exception as e:
            messagebox.showerror("Erreur de Connexion", f"Erreur lors de la connexion à la base de données : {e}")

    def create_labels(self):
        # Create labels on Canvas
        labels = [
            (28.0, 69.0, "Nom"),
            (28.0, 150.0, "Prénom"),
            (28.0, 231.0, "Numéro de téléphone"),
            (28.0, 312.0, "Email"),
            (394.0, 69.0, "Recherche"),
            (394.0, 150.0, "Date d'adhésion")
        ]
        for x, y, text in labels:
            self.canvas.create_text(x, y, anchor="nw", text=text, fill="#FFFFFF", font=("Inter Medium", 20 * -1))

    def create_buttons(self):
        # Create buttons
        buttons = [
            ("Ajouter", self.ajouter_membre, 144.0, 705.0),
            ("Modifier", self.modifier_membre, 515.0, 705.0),
            ("Supprimer", self.supprimer_membre, 886.0, 705.0),
            ("Rechercher", self.rechercher_membre, 997.0, 93.0)
        ]
        for text, command, x, y in buttons:
            button = ctk.CTkButton(self, text=text, command=command, width=250, height=50)
            button.place(x=x, y=y)

    def create_listview(self):
        # Create Treeview and Scrollbar
        self.listview = Treeview(self, columns=["ID", "Nom", "Prénom", "Téléphone", "Email", "Date d'adhésion"], show="headings")
        self.listview.place(x=28.0, y=418.0, width=1219.0, height=268.0)
        for col in ["ID", "Nom", "Prénom", "Téléphone", "Email", "Date d'adhésion"]:
            self.listview.heading(col, text=col)

        scrollbar = Scrollbar(self, orient="vertical", command=self.listview.yview)
        scrollbar.place(x=1247.0, y=418.0, height=268.0)
        self.listview.config(yscrollcommand=scrollbar.set)
        self.listview.bind("<<TreeviewSelect>>", self.on_item_selected)

    def load_data(self):
        # Load data from database
        try:
            data = self.db_connection.execute_query("SELECT * FROM Membres;")
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
                self.entry_nom.delete(0, "end")
                self.entry_nom.insert(0, item_values[1])
                self.entry_prenom.delete(0, "end")
                self.entry_prenom.insert(0, item_values[2])
                self.entry_telephone.delete(0, "end")
                self.entry_telephone.insert(0, item_values[3])
                self.entry_email.delete(0, "end")
                self.entry_email.insert(0, item_values[4])
                self.entry_date.set_date(item_values[5])

    def ajouter_membre(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        telephone = self.entry_telephone.get()
        email = self.entry_email.get()
        date_adhesion = self.entry_date.get()

        # Convertir la date en chaîne de caractères
        try:
            date_adhesion = datetime.strptime(date_adhesion, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError as e:
            messagebox.showerror("Erreur", f"Format de date invalide: {e}")
            return

        if nom and prenom and telephone and email and date_adhesion:
            try:
                query = "INSERT INTO Membres (nom, prenom, telephone, email, date_adhesion) VALUES (%s, %s, %s, %s, %s)"
                
                # Exécuter la requête d'insertion
                rows_affected = self.db_connection.execute_query(query, (nom, prenom, telephone, email, date_adhesion))
                
                # Check if insertion was successful
                if rows_affected > 0:
                    messagebox.showinfo("Information", "Membre ajouté avec succès.")
                    self.load_data()  # Mettre à jour la Treeview après l'ajout du membre
                else:
                    messagebox.showerror("Erreur", "Aucun membre n'a été ajouté.")
            except Exception as e:
                error_message = f"Erreur lors de l'ajout du membre: {e}"
                print(error_message)  # You can also log this error
                messagebox.showerror("Erreur", error_message)
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs nécessaires.")


    def modifier_membre(self):
        selected_item = self.listview.selection()
        if selected_item:
            nom = self.entry_nom.get()
            prenom = self.entry_prenom.get()
            telephone = self.entry_telephone.get()
            email = self.entry_email.get()
            date_adhesion = self.entry_date.get()

            if nom and prenom and telephone and email and date_adhesion:
                try:
                    item_values = self.listview.item(selected_item, "values")
                    member_id = item_values[0]
                    query = "UPDATE Membres SET nom = %s, prenom = %s, telephone = %s, email = %s, date_adhesion = %s WHERE id = %s"
                    self.db_connection.execute_query(query, (nom, prenom, telephone, email, date_adhesion, member_id))
                    messagebox.showinfo("Information", "Le membre a été modifié avec succès.")
                    self.load_data()  # Mettre à jour la Treeview après la modification du membre
                except Exception as e:
                    error_message = f"Erreur lors de la modification du membre: {e}"
                    print(error_message)  # Vous pouvez également écrire dans un fichier de log
                    messagebox.showerror("Erreur", error_message)
            else:
                messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs nécessaires.")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un membre à modifier.")




    def supprimer_membre(self):
        # Delete member from database
        selected_item = self.listview.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce membre ?")
            if confirmation:
                try:
                    item_values = self.listview.item(selected_item, "values")
                    member_id = item_values[0]
                    query = "DELETE FROM Membres WHERE id = %s"
                    self.db_connection.execute_query(query, (member_id,))
                    messagebox.showinfo("Information", "Le membre a été supprimé avec succès.")
                    self.observer.check_for_updates_members()  # Notify observers
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la suppression du membre: {e}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un membre.")

    def rechercher_membre(self, event=None):
        # Search for member in database
        recherche = self.entry_recherche.get()
        query = "SELECT * FROM Membres WHERE nom LIKE %s OR prenom LIKE %s OR telephone LIKE %s OR email LIKE %s OR date_adhesion LIKE %s"
        try:
            data = self.db_connection.execute_query(query, (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%", f"%{recherche}%"))
            self.update_listview(data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche de membres: {e}")

    def update(self, data):
        # Observer update method to refresh data in Treeview
        self.update_listview(data)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1280x773")
    widget = MemberManagementWidget(root)
    widget.pack(fill="both", expand=True)
    root.resizable(False, False)
    root.mainloop()
