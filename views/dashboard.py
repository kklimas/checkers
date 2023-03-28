import tkinter.ttk

from views.game import GameView
from views.settings import SettingsView
from views.view import *


class Dashboard(tk.Frame):
    def __init__(self, root, i18n_service):
        tk.Frame.__init__(self, root)

        self.root = root
        self.i18n = i18n_service
        self.root.title(self.i18n.get('app.title'))

        # translation
        self.init_dashboard()

    def init_dashboard(self):
        p1 = GameView(self, self.i18n)
        p2 = SettingsView(self, self.i18n)

        main_frame = tk.Frame(self)
        main_frame.configure(width=1000, height=600, bg='#312E2B')
        main_frame.grid(row=0, column=0)

        button_frame = tk.Frame(self)
        button_frame.configure(width=200, height=600, bg='#312E2B')
        button_frame.grid(row=0, column=1)

        # layout
        style = tkinter.ttk.Style()
        style.configure('menu-btn', bg='#356E2B')

        b1 = tk.Button(button_frame, text=self.i18n.get('app.menu.game.user'), command=p1.show)
        b2 = tk.Button(button_frame, text=self.i18n.get('app.menu.settings.title'), command=p2.show)

        p1.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=self, x=0, y=0, relwidth=1, relheight=1)

        b1.grid(row=0, column=0)
        b2.grid(row=1, column=0)
