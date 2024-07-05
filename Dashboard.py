from pathlib import Path
from tkinter import Tk, Canvas, Frame, Toplevel
import customtkinter as ctk
from Utilisateurs import UserManagementWidget
from Categorie import CategoryManagementWidget
from Membre import MemberManagementWidget
from Pret import LoanManagementWidget 
from Livres import BookManagementWidget  # Assuming UserManagementWidget is correctly implemented in Utilisateurs.py

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("/home/fabien/Documents/Projet/Projet Mida/Library pyhton project/build/assets/frame1")

class DashboardWidget(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.configure(bg="#282828")
        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self, bg="#282828", height=773, width=1280, bd=0, highlightthickness=0, relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Menu bar
        self.canvas.create_rectangle(0.0, 0.0, 277.0, 773.0, fill="#313131", outline="")
        self.canvas.create_rectangle(0.0, 0.0, 277.0, 51.0, fill="#217FC4", outline="")
        self.canvas.create_text(26.0, 3.0, anchor="nw", text="Menu", fill="#E2E2E2", font=("Inter Bold", 32 * -1))

        # Buttons
        #button_1 = ctk.CTkButton(self, text="Button 1", command=lambda: print("button_1 clicked"), width=263, height=40)
        #button_1.place(x=7.0, y=712.0)

        button_2 = ctk.CTkButton(self, text="Utilisateurs", width=250, height=40, command=self.open_user_management_widget)
        button_2.place(x=13.0, y=294.0)

        button_3 = ctk.CTkButton(self, text="Pret de livres", command=self.open_book_pret_categorie, width=250, height=40)
        button_3.place(x=13.0, y=180.0)

        button_4 = ctk.CTkButton(self, text="membres", command=self.open_book_member_categorie, width=250, height=40)
        button_4.place(x=13.0, y=237.0)

        button_5 = ctk.CTkButton(self, text="livres", command=self.open_book_livres_categorie, width=250, height=40)
        button_5.place(x=13.0, y=72.0)

        button_6 = ctk.CTkButton(self, text="Catégorie", command=self.open_book_category_widget, width=250, height=40)
        button_6.place(x=13.0, y=126.0)

        # Dashboard sections
        self.canvas.create_text(308.0, 14.0, anchor="nw", text="Tableau de bord ", fill="#E2E2E2", font=("Inter Bold", 32 * -1))
        self.canvas.create_rectangle(11.0, 49.0, 263.0, 51.0, fill="#FFFFFF", outline="")
        self.canvas.create_rectangle(308.0, 82.0, 596.0, 326.0, fill="#313131", outline="")
        self.canvas.create_rectangle(640.0, 78.0, 928.0, 322.0, fill="#313131", outline="")
        self.canvas.create_rectangle(972.0, 74.0, 1260.0, 318.0, fill="#313131", outline="")

        self.canvas.create_text(316.0, 87.0, anchor="nw", text="Livres disponibles", fill="#E2E2E2", font=("Inter Bold", 20 * -1))
        self.canvas.create_text(648.0, 83.0, anchor="nw", text="Nombre de membres", fill="#E2E2E2", font=("Inter Bold", 20 * -1))
        self.canvas.create_text(980.0, 79.0, anchor="nw", text="Nombres d'emprunt", fill="#E2E2E2", font=("Inter Bold", 20 * -1))

        Livres_dispo = self.canvas.create_text(322.0, 252.0, anchor="nw", text="10000", fill="#E2E2E2", font=("Inter Bold", 20 * -1))
        Livres_dispo = self.canvas.create_text(654.0, 248.0, anchor="nw", text="10000", fill="#E2E2E2", font=("Inter Bold", 20 * -1))
        self.canvas.create_text(986.0, 244.0, anchor="nw", text="10000", fill="#E2E2E2", font=("Inter Bold", 20 * -1))

    def open_user_management_widget(self):
        user_management_window = Toplevel(self.master)
        user_management_window.geometry("1280x773")
        user_management_widget = UserManagementWidget(user_management_window)
        user_management_widget.pack(fill="both", expand=True)

    def open_book_category_widget(self):
        user_management_window = Toplevel(self.master)
        user_management_window.geometry("1280x773")
        user_management_widget = CategoryManagementWidget(user_management_window)
        user_management_widget.pack(fill="both", expand=True)

    def open_book_member_categorie(self):
        user_management_window = Toplevel(self.master)
        user_management_window.geometry("1280x773")
        user_management_widget = MemberManagementWidget(user_management_window)
        user_management_widget.pack(fill="both", expand=True)

    def open_book_pret_categorie(self):
        user_management_window = Toplevel(self.master)
        user_management_window.geometry("1280x773")
        user_management_widget = LoanManagementWidget(user_management_window)
        user_management_widget.pack(fill="both", expand=True)

    def open_book_livres_categorie(self):
        user_management_window = Toplevel(self.master)
        user_management_window.geometry("1280x773")
        user_management_widget = BookManagementWidget(user_management_window)
        user_management_widget.pack(fill="both", expand=True)

    
    
    #BookManagementWidget
        
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

    root = Tk()
    root.geometry("1280x773")
    root.configure(bg="#282828")

    dashboard = DashboardWidget(root)
    dashboard.pack(fill="both", expand=True)

    root.resizable(False, False)
    root.mainloop()
