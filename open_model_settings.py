def open_model_settings(self):
    model_selection = simpledialog.askstring("Sélection du modèle", "Choisissez un modèle:\n" + "\n".join(self.models),
                                              initialvalue=self.model)
    if model_selection in self.models:
        self.model_var.set(model_selection)  # Met à jour le modèle sélectionné
        self.model = model_selection  # Met à jour l'attribut `self.model`
        messagebox.showinfo("Modèle", f"Modèle sélectionné: {model_selection}")
    else:
        messagebox.showwarning("Avertissement", "Modèle non valide. Veuillez choisir un modèle valide.")