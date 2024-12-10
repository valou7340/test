import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, colorchooser
import threading
from settings import UserSettings
from tts_manager import TTSManager
from network import NetworkManager


class ChatbotInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Graphique du Chatbot")

        # Initialize user settings
        self.settings = UserSettings()
        self.settings.load()

        # Initialize TTS manager - Move this line before create_menu
        self.tts_manager = TTSManager()
        self.tts_enabled = True  # State variable for TTS

        # Create the menu
        self.create_menu()

        # Initialize network manager
        self.network_manager = NetworkManager()

        # Prompt for server URL
        self.network_manager.server_url = simpledialog.askstring("Serveur", "Entrez l'URL du serveur:",
                                                                 initialvalue="http://192.168.1.108:1234")
        if not self.network_manager.server_url:
            messagebox.showerror("Erreur", "URL du serveur non fournie. L'application va se fermer.")
            root.destroy()
            return

        # Prompt for model selection
        self.models = ["llama-3.2-3b-instruct:2", "autre-modèle-1", "autre-modèle-2"]
        self.model = simpledialog.askstring("Modèle", "Choisissez un modèle:", initialvalue=self.models[0])
        if self.model not in self.models:
            messagebox.showerror("Erreur", "Modèle non valide. L'application va se fermer.")
            root.destroy()
            return

        self.data = {"temperature": 0.5, "max_tokens": 4000}

        # Configure grid weights for responsive layout
        self.setup_layout()
        # Create widgets
        self.create_widgets()

        # Create TTS toggle button
        self.tts_toggle_button = tk.Button(self.root, text="Désactiver TTS", command=self.toggle_tts)
        self.tts_toggle_button.grid(row=1, column=0, padx=10, pady=5, sticky='w')  # Position the button

    def create_menu(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.root)

        # Model menu
        model_menu = tk.Menu(menu_bar, tearoff=0)
        model_menu.add_command(label="Paramètres du modèle", command=self.open_model_settings)
        menu_bar.add_cascade(label="Modèle", menu=model_menu)

        # Display menu
        display_menu = tk.Menu(menu_bar, tearoff=0)
        display_menu.add_command(label="Paramètres d'affichage", command=self.settings.open_display_settings)
        menu_bar.add_cascade(label="Affichage", menu=display_menu)

        # TTS menu
        tts_menu = tk.Menu(menu_bar, tearoff=0)
        tts_menu.add_command(label="Paramètres TTS", command=self.tts_manager.open_tts_settings)
        menu_bar.add_cascade(label="TTS", menu=tts_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="À propos", command=self.show_about)
        menu_bar.add_cascade(label="Aide", menu=help_menu)

        # Configure the menu bar
        self.root.config(menu=menu_bar)

    def open_model_settings(self):
        model_selection = simpledialog.askstring("Sélection du modèle",
                                                 "Choisissez un modèle:\n" + "\n".join(self.models),
                                                 initialvalue=self.model)
        if model_selection in self.models:
            self.model = model_selection  # Met à jour l'attribut `self.model`
            messagebox.showinfo("Modèle", f"Modèle sélectionné: {model_selection}")
        else:
            messagebox.showwarning("Avertissement", "Modèle non valide. Veuillez choisir un modèle valide.")

    def show_about(self):
        messagebox.showinfo("À propos", "Chatbot Interface\nVersion 1.0")

    def setup_layout(self):
        self.root.grid_rowconfigure(0, weight=1)  # Chat area
        self.root.grid_rowconfigure(1, weight=0)  # Message entry
        self.root.grid_columnconfigure(0, weight=1)  # Chat area
        self.root.grid_columnconfigure(1, weight=1)  # Model selection
        self.root.grid_columnconfigure(2, weight=0)  # Send button

    def create_widgets(self):
        # Frame for chat area
        chat_frame = tk.Frame(self.root)
        chat_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.response_text = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, bg=self.settings.bg_color,
                                                       font=self.settings.text_font, fg=self.settings.text_color)
        self.response_text.pack(expand=True, fill='both')

        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.model_label = tk.Label(control_frame, text="Modèle:")
        self.model_var = tk.StringVar(value=self.model)
        self.model_menu = tk.OptionMenu(control_frame, self.model_var, *self.models)
        self.message_label = tk.Label(control_frame, text="Message:")
        self.message_entry = tk.Entry(control_frame, width=40)
        self.send_button = tk.Button(control_frame, text="Envoyer", command=self.send_message)

        # Layout controls
        self.model_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.model_menu.grid(row=0, column=1, padx=5, pady=5)
        self.message_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.message_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.send_button.grid(row=1, column=2, padx=5, pady=5)

        # Bind Enter key to send message
        self.root.bind('<Return>', lambda event: self.send_message())

    def toggle_tts(self):
        self.tts_enabled = not self.tts_enabled  # Toggle the state
        if self.tts_enabled:
            self.tts_toggle_button.config(text="Désactiver TTS")  # Update button text
        else:
            self.tts_toggle_button.config(text="Activer TTS")  # Update button text

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            messagebox.showwarning("Avertissement", "Veuillez entrer un message.")
            return

        self.response_text.insert(tk.END, f"Vous: {message}\n")
        self.message_entry.delete(0, tk.END)

        # Start a new thread to handle the chatbot response
        threading.Thread(target=self.get_chatbot_response, args=(message,)).start()

    def get_chatbot_response(self, message):
        response = self.network_manager.get_response(self.model, message, self.data)
        self.root.after(0, self.update_chat, response)

    def update_chat(self, response):
        self.response_text.insert(tk.END, f"Chatbot: {response}\n")
        if self.tts_enabled:  # Check if TTS is enabled before speaking
            self.tts_manager.speak_text(response)