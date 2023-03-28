from views.view import *


class HomeView(View):
    def __init__(self, root, i18n_service):
        View.__init__(self, root, i18n_service)
        self.config(bg='black')
        label = tk.Label(self, text=self.i18n.get('app.menu.home.label'))
        label.pack(side="bottom", fill="both", expand=True)
