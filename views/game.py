import tkinter as tk

from views.view import View


class GameView(View):
    def __init__(self, root, i18n_service):
        View.__init__(self, root, i18n_service)
        self.configure(width=1200, height=600, bg='#312E2B')
        label = tk.Label(self, text=self.i18n.get('app.menu.game.label'))
        label.pack(side="top", fill="both", expand=True)
