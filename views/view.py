import tkinter as tk


class View(tk.Frame):
    def __init__(self, root, i18n_service, *args, **kwargs):
        tk.Frame.__init__(self, root)
        self.i18n = i18n_service

    def show(self):
        self.lift()
