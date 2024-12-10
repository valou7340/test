import pyttsx3
from tkinter import simpledialog, messagebox

class TTSManager:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.tts_voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', self.tts_voices[0].id)  # Default voice
        self.tts_rate = self.tts_engine.getProperty('rate')

    def speak_text(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def open_tts_settings(self):
        voice_names = [voice.name for voice in self.tts_voices]
        selected_voice_name = simpledialog.askstring("Choisir une voix",
                                                     "Choisissez une voix:", initialvalue=self.tts_voices[0].name)

        # Populate voice selection from available voices
        if selected_voice_name in voice_names:
            for voice in self.tts_voices:
                if voice.name == selected_voice_name:
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        else:
            messagebox.showwarning("Avertissement", "Voix non valide. Veuillez choisir une voix disponible.")

        rate = simpledialog.askinteger("Choisir la vitesse de parole", "Entrez la vitesse de parole (ex: 150):",
                                       initialvalue=self.tts_rate)
        if rate is not None:
            self.tts_engine.setProperty('rate', rate)