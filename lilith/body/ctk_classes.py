import customtkinter as ct
from PIL import Image
from customtkinter import CTkImage, CTkLabel
from routes import ROUTES
import os

class ImageFrame(ct.CTkFrame):
    def __init__(self, master, image_path, width=160, height=160, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.pack_propagate = False

        img = Image.open(image_path)
        self.ctk_img = CTkImage(light_image=img, size=(width, height))

        self.img_label = CTkLabel(self, image=self.ctk_img, text="")
        self.img_label.pack(expand=True, fill="both")


class ChatFrame(ct.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # chat scrollable
        self.chat_display = ct.CTkTextbox(self)
        self.chat_display.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.chat_display.configure(
            fg_color=("gray95", "#1A1A1A"),
            text_color=("black","white"),
            corner_radius=10,
            font=("Helvetica", 20),
            wrap="word",
            padx=5,
            pady=5,
            state="disabled" # en lecture seule
        )

        #text styles
        self.tetsuya_tag_config = {
            "foreground": "#007BFF",
            "justify": "right"
        }

        self.lilith_tag_config = {
            "foreground": "#28A745",
            "justify": "left"
        }

        self.message_tag_config = {
            "lmargin1": 20,
            "lmargin2": 20,
        }

    def add_tetsu_message(self, message):
        self.chat_display.configure(state="normal")
        # saut de ligne si nécessaire
        if self.chat_display.index("end-1c") != "1.0":
            self.chat_display.insert("end", "\n\n")

        # ajout en-tête
        self.chat_display.insert("end", "Tetsuya 乂 : ", "tetsuya")
        # contenu
        self.chat_display.insert("end", message, "tetsuya_message")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

        # config tags
        self.chat_display.tag_config("tetsuya", **self.tetsuya_tag_config)
        self.chat_display.tag_config("tetsuya_message", **self.message_tag_config)

    def add_lilith_message(self, message):
        self.chat_display.configure(state="normal")
        # saut de ligne si nécessaire
        if self.chat_display.index("end-1c") != "1.0":
            self.chat_display.insert("end", "\n\n")
        # ajout en-tête
        self.chat_display.insert("end", "Lilith ♥ : ", "lilith")
        # contenu
        self.chat_display.insert("end", message, "lilith_message")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

        # config tags
        self.chat_display.tag_config("lilith", **self.lilith_tag_config)
        self.chat_display.tag_config("lilith_message", **self.message_tag_config)

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")



class InputFrame(ct.CTkFrame):
    def __init__(self, master, submit_callback):
        super().__init__(master)
        self.submit_callback = submit_callback

        # Configuration pour que l'entrée prenne toute la largeur disponible
        self.grid_columnconfigure(0, weight=1)

        # Champ de saisie
        self.entry = ct.CTkEntry(self, placeholder_text="...")
        self.entry.grid(row=0, column=0, padx=(5, 2), pady=5, sticky="ew")
        self.entry.bind("<Return>", self.on_submit)

        # Bouton d'envoi
        self.submit_button = Button(self, value=">>", command=self.on_submit)
        self.submit_button.grid(row=0, column=1, padx=(2, 5), pady=5)

    def on_submit(self, event=None):  # Ajout du paramètre event pour gérer l'événement Return
        input_ = self.entry.get().strip()
        if input_:
            self.submit_callback(input_)
            self.entry.delete(0, "end")  # Clean entry
            return "break"  # Empêche le comportement par défaut de la touche Return

class ButtonFrame(ct.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        padx_frame = (5,2)
        pady_frame = 5

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.menu_button = Button(master=self, value="Menu", command=self.menu_callback)
        self.menu_button.grid(row=0, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.code_button = Button(master=self, value="Code", command=self.code_callback)
        self.code_button.grid(row=1, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.image_button = Button(master=self, value="Images", command=self.image_callback)
        self.image_button.grid(row=2, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.lilith_button = Button(master=self, value="Lilith", command=self.lilith_callback)
        self.lilith_button.grid(row=3, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.discussion_button = Button(master=self, value="Discussion", command=self.discussion_callback)
        self.discussion_button.grid(row=4, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.gestion_button = Button(master=self, value="Gestion fichiers", command=self.gestion_callback)
        self.gestion_button.grid(row=5, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.envoi_button = Button(master=self, value="Envoi données", command=self.envoi_callback)
        self.envoi_button.grid(row=6, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.crawl_button = Button(master=self, value="Crawling", command=self.crawl_callback)
        self.crawl_button.grid(row=7, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")

    def menu_callback(self):
        print("menu callback")

    def code_callback(self):
        print("code callback")

    def image_callback(self):
        print("image callback")

    def lilith_callback(self):
        print("lilith callback")

    def discussion_callback(self):
        print("discussion callback")

    def gestion_callback(self):
        print("gestion callback")

    def envoi_callback(self):
        print("envoi callback")

    def crawl_callback(self):
        print("crawl callback")


class Button(ct.CTkButton):
    def __init__(self, master, value, command):
        super().__init__(master)

        self.value = value
        self.command = command

        self.configure(
            text=self.value,
            fg_color=("black", "#000000"),
            text_color=("white", "#FFFFFF"),
            hover_color=("grey", "#292929"),
            corner_radius=10,
            font=('Cursive', 12, 'bold'),
            command=self.command,
        )


class LateralToolbar(ct.CTkFrame):
    def __init__(self, master, width=300):
        super().__init__(master, width=width)

        #empecher le redimensionnement
        self.grid_propagate(False)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.buttons_frame = ButtonFrame(self)
        self.buttons_frame.grid(row=0, column=0, sticky="nsew")
        self.img = ImageFrame(self, os.path.join(ROUTES["views/lilith"], "lilith_v1.png"), width=500, height=520, corner_radius=15)
        self.img.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

class App(ct.CTk):
    def __init__(self, text="Bonjour Tetsuya."):
        super().__init__()

        self.text_zone_text = text
        self.title("Lilith ♥")
        self.geometry("1200x800")

        # Utiliser pack au lieu de grid pour le layout principal

        # Frame principal qui contient tout
        self.main_frame = ct.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # Configuration des colonnes et lignes du main_frame
        self.main_frame.grid_columnconfigure(0, weight=0)  # Colonne de la barre latérale
        self.main_frame.grid_columnconfigure(1, weight=1)  # Colonne principale
        self.main_frame.grid_rowconfigure(0, weight=1)  # Ligne du chat

        # Barre d'outils latérale
        self.lateral_toolbar = LateralToolbar(self.main_frame)
        self.lateral_toolbar.grid(row=0, column=0, padx=5, pady=5, sticky="nsw")

        # Frame pour le chat et l'input
        self.chat_input_frame = ct.CTkFrame(self.main_frame, fg_color="transparent")
        self.chat_input_frame.grid(row=0, column=1, sticky="nsew")
        self.chat_input_frame.grid_columnconfigure(0, weight=1)
        self.chat_input_frame.grid_rowconfigure(0, weight=1)
        self.chat_input_frame.grid_rowconfigure(1, weight=0)

        # Zone de chat
        self.chat_frame = ChatFrame(self.chat_input_frame)
        self.chat_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Message de bienvenue
        self.chat_frame.add_lilith_message("Bonjour Tetsuya, que veux tu faire aujourd'hui ?")

        # Zone d'entrée
        self.input_frame = InputFrame(self.chat_input_frame, self.process_message)
        self.input_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def process_message(self, question):
        """point d'entrée pour la réponse de Lilith"""
        # mon message
        self.chat_frame.add_tetsu_message(question)
        # lilith traite la réponse
        answer = self.generate_answer(question)
        # affichage de sa réponse
        self.chat_frame.add_lilith_message(answer)

    def generate_answer(self, question):
        """Génère une réponse basée sur le message de l'utilisateur"""
        # Exemple simple - à remplacer par votre logique d'IA
        if "bonjour" in question.lower() or "salut" in question.lower():
            return "Bonjour Tetsuya, bien dormi ?"
        elif "aide" in question.lower():
            return "Je peux t'aider pour tout ce que tu veux, précise moi ta question."
        elif "merci" in question.lower():
            return "Je t'en prie, tu veux encore de l'aide sur quelque chose ?"
        else:
            return f"J'ai bien reçu ton message : '{question}'."


