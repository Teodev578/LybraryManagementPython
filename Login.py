import customtkinter as ctk
from tkinter import Canvas, PhotoImage, messagebox
import mysql.connector
from pathlib import Path
from Dashboard import DashboardWidget

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path

class LoginWidget(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#282828")
        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self, bg="#282828", height=385, width=708, bd=0, highlightthickness=0, relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_text(
            375.0, 41.0, anchor="nw", text="Connexion", fill="#FFFFFF", font=("Inter Bold", 32 * -1)
        )

        self.entry_1 = ctk.CTkEntry(
            master=self, width=280, height=38, border_color="#282828", corner_radius=5
        )
        self.entry_1.place(x=385.0, y=127.0)

        self.entry_2 = ctk.CTkEntry(
            master=self, width=280, height=38, border_color="#282828", corner_radius=5, show="*"
        )
        self.entry_2.place(x=385.0, y=215.0)

        self.canvas.create_text(
            375.0, 91.0, anchor="nw", text="Utilisateur", fill="#FFFFFF", font=("Inter Medium", 12 * -1)
        )

        self.canvas.create_text(
            375.0, 181.0, anchor="nw", text="Mot de passe", fill="#FFFFFF", font=("Inter Medium", 12 * -1)
        )

        self.button_1 = ctk.CTkButton(
            master=self, text="Se connecter", width=280, height=40, corner_radius=5, command=self.login
        )
        self.button_1.place(x=385.0, y=303.0)

        self.canvas.create_rectangle(
            0.0, 0.0, 334.0, 385.0, fill="#217FC4", outline=""
        )

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(172.0, 261.0, image=self.image_image_1)

        self.canvas.create_text(
            20.0, 30.0, anchor="nw", text="Bienvenue à vous!", fill="#FFFFFF", font=("Inter Bold", 36 * -1)
        )

    def login(self):
        username = self.entry_1.get()
        password = self.entry_2.get()

        try:
            db_connection = mysql.connector.connect(
                host="localhost", user="root", password="OKok__1325__", database="Lybrary"
            )

            cursor = db_connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                messagebox.showinfo("Connexion réussie", "Vous êtes connecté avec succès !")
                self.open_dashboard()
            else:
                messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect")
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur : {e}")

    def open_dashboard(self):
        # Destroy the login widget first
        self.destroy()
        # Then create and display the dashboard
        dashboard = DashboardWidget(self.master)
        dashboard.pack(fill="both", expand=True)
