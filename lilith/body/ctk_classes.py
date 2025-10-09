import customtkinter as ct
from PIL import Image
from customtkinter import CTkImage, CTkLabel
from routes import ROUTES, path_to_module
import os
import importlib
import threading
import time

lilith_mind_discussion = ROUTES["lilith-mind-discussion"]
lilith_mind_discussion = path_to_module(lilith_mind_discussion)

try:
    discussion_agent = importlib.import_module(lilith_mind_discussion)
except Exception as e:
    print(f"Erreur lors de l'import du module : {e}")
    raise

load_model = discussion_agent.load_model
process_answer = discussion_agent.process_answer

pipe = load_model()

class ImageFrame(ct.CTkFrame):
    def __init__(self, master, image_path, width=160, height=160, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.pack_propagate(False)

        img = Image.open(image_path)
        self.ctk_img = CTkImage(light_image=img, size=(width, height))

        self.img_label = CTkLabel(self, image=self.ctk_img, text="")
        self.img_label.pack(expand=True, fill="both")

class ChatFrame(ct.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.chat_display = ct.CTkTextbox(self)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.chat_display.configure(
            fg_color=("gray95", "#1A1A1A"),
            text_color=("black","white"),
            corner_radius=10,
            font=("Helvetica", 18),
            wrap="word",
            padx=10,
            pady=10,
            state="disabled"
        )

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

        self.loading = False
        self.loading_line_index = None
        self.loading_animation_id = None

    def add_tetsu_message(self, message):
        self.chat_display.configure(state="normal")
        if self.chat_display.index("end-1c") != "1.0":
            self.chat_display.insert("end", "\n\n")
        self.chat_display.insert("end", "Tetsuya 乂 : ", "tetsuya")
        self.chat_display.insert("end", message, "tetsuya_message")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

        self.chat_display.tag_config("tetsuya", **self.tetsuya_tag_config)
        self.chat_display.tag_config("tetsuya_message", **self.message_tag_config)

    def add_lilith_message(self, message):
        self.chat_display.configure(state="normal")
        if self.chat_display.index("end-1c") != "1.0":
            self.chat_display.insert("end", "\n\n")
        self.chat_display.insert("end", "Lilith ♥ : ", "lilith")
        self.chat_display.insert("end", message, "lilith_message")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

        self.chat_display.tag_config("lilith", **self.lilith_tag_config)
        self.chat_display.tag_config("lilith_message", **self.message_tag_config)

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")

    def start_loading(self):
        """Affiche et anime 'Lilith ♥ : ...'"""
        if self.loading:
            return
        self.loading = True
        self.chat_display.configure(state="normal")
        if self.chat_display.index("end-1c") != "1.0":
            self.chat_display.insert("end", "\n\n")
        self.chat_display.insert("end", "Lilith ♥ : ", "lilith")
        self.loading_line_index = self.chat_display.index("end-1c")
        self.chat_display.insert("end", "...", "lilith_message")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        self.dots_count = 0
        self.animate_loading()

    def animate_loading(self):
        if not self.loading:
            return
        self.dots_count = (self.dots_count + 1) % 4  # 0,1,2,3
        dots = "." * self.dots_count
        self.chat_display.configure(state="normal")
        start = f"{self.loading_line_index} linestart + 11 chars"
        end = f"{self.loading_line_index} linestart + 14 chars"
        self.chat_display.delete(start, end)
        self.chat_display.insert(start, dots, "lilith_message")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        self.loading_animation_id = self.after(300, self.animate_loading)

    def stop_loading(self):
        if not self.loading:
            return
        self.loading = False
        if self.loading_animation_id:
            self.after_cancel(self.loading_animation_id)
            self.loading_animation_id = None
        self.chat_display.configure(state="normal")
        start_line = f"{self.loading_line_index} linestart"
        end_line = f"{self.loading_line_index} lineend + 1 char"
        self.chat_display.delete(start_line, end_line)
        self.chat_display.configure(state="disabled")

class InputFrame(ct.CTkFrame):
    def __init__(self, master, submit_callback):
        super().__init__(master)
        self.submit_callback = submit_callback

        self.grid_columnconfigure(0, weight=1)

        self.entry = ct.CTkEntry(self, placeholder_text="Écris ton message ici...")
        self.entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.entry.bind("<Return>", self.on_submit)

        self.submit_button = ct.CTkButton(self, text="Envoyer", command=self.on_submit)
        self.submit_button.grid(row=0, column=1, padx=(5, 10), pady=10)

    def on_submit(self, event=None):
        input_ = self.entry.get().strip()
        if input_:
            self.submit_callback(input_)
            self.entry.delete(0, "end")
            return "break"

class ButtonFrame(ct.CTkFrame):
    def __init__(self,master,chat_frame):
        super().__init__(master)
        self.chat_frame = chat_frame

        padx_frame = (5,2)
        pady_frame = 5

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.code_button = Button(master=self, value="Code", command=self.code_callback)
        self.code_button.grid(row=1, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.image_button = Button(master=self, value="Images", command=self.image_callback)
        self.image_button.grid(row=2, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.discussion_button = Button(master=self, value="Discussion", command=self.discussion_callback)
        self.discussion_button.grid(row=4, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.gestion_button = Button(master=self, value="Gestion fichiers", command=self.gestion_callback)
        self.gestion_button.grid(row=5, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.envoi_button = Button(master=self, value="Envoi données", command=self.envoi_callback)
        self.envoi_button.grid(row=6, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")
        self.crawl_button = Button(master=self, value="Crawling", command=self.crawl_callback)
        self.crawl_button.grid(row=7, column=0, padx=padx_frame, pady=pady_frame, sticky="ew")

    #########################################" CALLBACKS "#####################################################

    def code_callback(self):
        self.chat_frame.clear_chat()
        self.chat_frame.add_lilith_message(message="Tu as choisi l'option pour des questions de code.")
        print("code callback")

    def image_callback(self):
        self.chat_frame.clear_chat()
        self.chat_frame.add_lilith_message(message="Tu as choisi l'option pour des questions de images.")
        print("image callback")

    def discussion_callback(self):
        self.chat_frame.clear_chat()
        self.chat_frame.add_lilith_message(message="Tu as choisi l'option pour une discussion avec moi.")
        print("discussion callback")

    def gestion_callback(self):
        self.chat_frame.clear_chat()
        self.chat_frame.add_lilith_message(message="Tu as choisi l'option de gestion de fichiers.")
        print("gestion callback")

    def envoi_callback(self):
        self.chat_frame.clear_chat()
        self.chat_frame.add_lilith_message(message="Tu as choisi l'option pour l'envoi de données.")
        print("envoi callback")

    def crawl_callback(self):
        self.chat_frame.clear_chat()
        self.chat_frame.add_lilith_message(message="Tu as choisi l'option pour du crawl sur le web.")
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
    def __init__(self, master, chat_frame, width=300):
        super().__init__(master, width=width)

        self.grid_propagate(False)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.buttons_frame = ButtonFrame(self,chat_frame)
        self.buttons_frame.grid(row=0, column=0, sticky="nsew")
        self.img = ImageFrame(self, os.path.join(ROUTES["views/lilith"], "zoe_kpop.jpg"), width=500, height=520, corner_radius=15)
        self.img.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

class App(ct.CTk):
    def __init__(self, text="Bonjour Tetsuya."):
        super().__init__()

        self.text_zone_text = text
        self.title("Lilith ♥")
        self.geometry("1200x800")

        self.main_frame = ct.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.chat_input_frame = ct.CTkFrame(self.main_frame, fg_color="transparent")
        self.chat_input_frame.grid(row=0, column=1, sticky="nsew")
        self.chat_input_frame.grid_columnconfigure(0, weight=1)
        self.chat_input_frame.grid_rowconfigure(0, weight=1)
        self.chat_input_frame.grid_rowconfigure(1, weight=0)

        self.chat_frame = ChatFrame(self.chat_input_frame)
        self.chat_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.lateral_toolbar = LateralToolbar(self.main_frame,self.chat_frame)
        self.lateral_toolbar.grid(row=0, column=0, padx=5, pady=5, sticky="nsw")

        self.chat_frame.add_lilith_message("Bonjour Tetsuya, que veux tu faire aujourd'hui ?")

        self.input_frame = InputFrame(self.chat_input_frame, self.process_message)
        self.input_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def process_message(self, question):
        self.chat_frame.add_tetsu_message(question)
        self.chat_frame.start_loading()

        def worker():
            answer = self.generate_answer(question)
            self.after(0, self.display_answer, answer)

        threading.Thread(target=worker, daemon=True).start()

    def display_answer(self, answer):
        self.chat_frame.stop_loading()
        self.chat_frame.add_lilith_message(answer)

    def generate_answer(self, question):
        return process_answer(question, pipe)
