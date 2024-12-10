import json  
import os  
from tkinter import simpledialog, colorchooser, messagebox

class UserSettings:
    def __init__(self):
        self.bg_color = "white"
        self.text_color = "black"
        self.text_font = ("Arial", 12)

    def load(self):
        if os.path.exists("user_settings.json"):
            with open("user_settings.json", "r") as f:
                settings = json.load(f)
                self.bg_color = settings.get("bg_color", "white")
                self.text_color = settings.get("text_color", "black")
                self.text_font = tuple(settings.get("text_font", ("Arial", 12)))

    def save(self):
        settings = {
            "bg_color": self.bg_color,
            "text_color": self.text_color,
            "text_font": self.text_font  
        }
        with open("user_settings.json", "w") as f:
            json.dump(settings, f)

    def open_display_settings(self):
        if messagebox.askyesno("Personnalisation", "Voulez-vous personnaliser l'affichage?"):
            bg_color = colorchooser.askcolor(title="Choisissez une couleur de fond")[1]
            text_color = colorchooser.askcolor(title="Choisissez une couleur de texte")[1]
            font_name = simpledialog.askstring("Choisir la police", "Entrez le nom de la police (ex: Arial):",
                                               initialvalue="Arial")
            font_size = simpledialog.askinteger("Choisir la taille de la police", "Entrez la taille de la police:",
                                                initialvalue=12)
            if bg_color and text_color and font_name and font_size:
                self.bg_color = bg_color  
                self.text_color = text_color  
                self.text_font = (font_name, font_size)
                self.save()