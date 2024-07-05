import customtkinter
import tkinter as tk
import customtkinter as ctk
from Login import LoginWidget
from Dashboard import DashboardWidget

# Exemple d'utilisation du widget dans une fenêtre principale
if __name__ == "__main__":
    # Initialisation de la fenêtre principale avec CustomTkinter
    window = ctk.CTk()

    window.geometry("708x385")
    #window.configure(fg_color="#282828")  # Utilisation de fg_color au lieu de bg
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    # Instanciation du widget personnalisé
    widget = LoginWidget(window)
    widget.pack(fill="both", expand=True)
    
    window.mainloop()
