import tkinter as tk

from service.i18n_service import I18NService
from views.dashboard import Dashboard


class App:
    def __init__(self):
        self.i18n_service = I18NService()
        root = tk.Tk()
        main = Dashboard(root, self.i18n_service)
        main.pack(side="top", fill="both", expand=True)
        root.resizable(False, False)
        root.wm_geometry("1200x600")
        root.mainloop()


if __name__ == '__main__':
    App()

