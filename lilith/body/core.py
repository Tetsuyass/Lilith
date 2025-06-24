from . import (App)

class Core:
    def __init__(self):
        self.ctk_uid = App()

    def start_(self):
        self.ctk_uid.mainloop()