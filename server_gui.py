import sys
from tkinter import *
import threading
from app import start_flask # Importez la fonction start_flask
import os

GUI_BACKGROUND = "#1f2029"
GUI_BACKGROUND_2 = "#16171d"
GUI_FOREGROUND = "#ffffff"
GUI_PRIMARY = "#ff8e47"

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, message)
        self.text_widget.see(END)
        self.text_widget.config(state=DISABLED)

    def flush(self):
        pass 

server_thread = None  # Référence au thread du serveur

def startbtn():
    global server_thread
    if server_thread is None or not server_thread.is_alive():  # Vérifiez si le serveur n'est pas déjà en cours
        server_thread = threading.Thread(target=start_flask)  # Créez un nouveau thread
        server_thread.start()  # Démarrez le serveur Flask dans un thread
        info_label.config(text="Serveur allumé", bg="#2f3c38", fg="#ffffff", highlightbackground="#9eff9e", highlightcolor="#9eff9e")

def stopbtn():
    os._exit(0)
    root.quit()
    exit()
    global server_thread
    if server_thread is not None and server_thread.is_alive():  # Vérifiez si le serveur est en cours d'exécution
        info_label.config(text="Serveur éteint", bg="#3b2231", fg="#ffffff", highlightbackground="#ff3668", highlightcolor="#ff3668")
    else:
        print("Le serveur n'est pas en cours d'exécution.")

# ? setup window
guipyhwa = Tk()
guipyhwa.geometry("1200x550") 
guipyhwa.title("PyHwa GUI")
guipyhwa.config(bg=GUI_BACKGROUND)
guipyhwa.resizable(False, False)
guipyhwa.iconbitmap("static/img/favicon.ico")
# icon = PhotoImage(file="static/img/favicon.ico")
# guipyhwa.iconphoto(False, icon)


# ? Configure grid layout
guipyhwa.grid_columnconfigure(0, weight=1)
guipyhwa.grid_columnconfigure(1, weight=3)

# ? Left side frame (Titre, Boutons, Info label)
left_frame = Frame(guipyhwa, bg=GUI_BACKGROUND)
left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

title_label = Label(left_frame, text="PyHwa GUI server interface", font=("Arial", 18), bg=GUI_BACKGROUND, fg=GUI_FOREGROUND)
title_label.pack(pady=10)

start_button = Button(left_frame, text="Démarrage", font=("Arial", 18), bg=GUI_PRIMARY, fg=GUI_FOREGROUND, bd=0, command=startbtn)
start_button.pack(pady=10, fill=X)

stop_button = Button(left_frame, text="Stop", font=("Arial", 18), bg=GUI_PRIMARY, fg=GUI_FOREGROUND, bd=0, command=stopbtn)
stop_button.pack(pady=10, fill=X)

# ? Info label avec styles
info_label = Label(
    left_frame,
    text="Serveur éteint",
    font=("Arial", 18),
    bg="#2f3c38", 
    fg="#ffffff",
    bd=0, 
    highlightbackground="#9eff9e", 
    relief="solid", 
    padx=10,
    pady=10,
    highlightthickness=2,
)
info_label.pack(pady=10, fill=X)
info_label.config(highlightbackground="#9eff9e", highlightcolor="#9eff9e")

# ? Right side (self_output for console output)
self_output = Text(guipyhwa, wrap="word", font=("Arial", 14), bg=GUI_BACKGROUND_2, fg=GUI_FOREGROUND, bd=0)
self_output.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

self_output.config(state=DISABLED)

sys.stdout = ConsoleRedirector(self_output)

# ? start
guipyhwa.mainloop()
