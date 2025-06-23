import customtkinter as ct

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
            font=("Helvetica", 12),
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
        self.chat_display.insert("end", "Tetsuya: ", "tetsuya")
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
        self.chat_display.insert("end", "Lilith: ", "lilith")
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


class TextZoneFrame(ct.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.zone = TextZone(self)
        self.zone.grid(row=0, column=0,
                       sticky="nsew")
        self.zone.insert(0.0, text)


class TextZone(ct.CTkTextbox):
    def __init__(self, master):
        super().__init__(master)

        self.configure(
            fg_color=("black", "#000000"),
            text_color=("white", "#FFFFFF"),
            corner_radius=10,
            font=('Cursive', 12, 'bold'),
        )


class LateralToolbar(ct.CTkFrame):
    def __init__(self, master, width=200):
        super().__init__(master, width=width)

        #empecher le redimensionnement
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)

        self.checkbox_1 = ct.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = ct.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_3 = ct.CTkCheckBox(self, text="checkbox 3")
        self.checkbox_3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

    def get(self):
        checked = []
        if self.checkbox_1.get() == 1:
            checked.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked.append(self.checkbox_2.cget("text"))
        if self.checkbox_3.get() == 1:
            checked.append(self.checkbox_3.cget("text"))
        return checked

    def menu(self):
        print("Bouton menu pressé.")

    def settings(self):
        print("Bouton paramètres pressé.")

    def history(self):
        print("Bouton historique pressé")

class App(ct.CTk):
    def __init__(self, text="Bonjour Tetsuya."):
        super().__init__()

        self.text_zone_text = text
        self.title("Lilith ♥")
        self.geometry("700x600")

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
        self.input_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

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
            return "Bonjour Tetusya, bien dormi ?"
        elif "aide" in question.lower():
            return "Je peux t'aider pour tout ce que tu veux, précise moi ta question."
        elif "merci" in question.lower():
            return "Je t'en prie, tu veux encore de l'aide sur quelque chose ?"
        else:
            return f"J'ai bien reçu ton message : '{question}'."


