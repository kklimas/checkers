from src.main.model.statistics import Statistics
from src.resources.constants import WIDTH, FONT_TITLE, FONT, WHITE, RESULTS_FONT


class HistoryView:
    def __init__(self, window, i18n_provider):
        self.i18n = i18n_provider
        self.window = window
        self.font_title = FONT_TITLE
        self.font = FONT
        self.latest_results = Statistics().get_latest_results()
        self.__clean_up_results()

        self.draw()

    def __clean_up_results(self):
        self.latest_results = [line[:-1] for line in self.latest_results if '----\n' not in line][-6:]

    def draw(self):
        self._draw_labels()

    def _draw_labels(self):
        self._center(0, WIDTH, 10, 'history', True)
        self.__draw_results()

    def _center(self, x1, x2, y, key, title_font=False):
        label, font = self._get_label(key, title_font)
        text_width, _ = font.size(self._get(key))
        block_width = x2 - x1

        if text_width < block_width:
            x1 = (block_width - text_width) // 2 + x1
        else:
            x1 -= (text_width - block_width) // 2
        self.window.blit(label, (x1, y))

    def _get_label(self, key, title_font=True):
        if title_font:
            return self.font_title.render(self._get(key), 1, WHITE), self.font_title
        return self.font.render(self._get(key), 1, WHITE), self.font

    def _get(self, key):
        return self.i18n.get('app.menu.' + key)

    def __draw_results(self):
        for index, line in enumerate(self.latest_results):
            results_font = RESULTS_FONT.render(line, 1, WHITE)
            self.window.blit(results_font, (350, index * 40 + 80))
