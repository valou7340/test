import tkinter as tk  
from chatbot_interface import ChatbotInterface

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_interface = ChatbotInterface(root)
    root.mainloop()