import tkinter as tk

from views.view import View


class SettingsView(View):
    def __init__(self, root, i18n_service):
        View.__init__(self, root, i18n_service)
        label = tk.Label(self, text=self.i18n.get('app.menu.settings.label'))
        label.pack(side="top", fill="both", expand=True)
