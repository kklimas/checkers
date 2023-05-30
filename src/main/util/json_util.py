import json

from src.main.model.game_mode import GameMode
from src.resources.constants import CONFIG_FILE_PATH


class JsonUtil:
    def __init__(self):
        self.file_path = CONFIG_FILE_PATH

    def get_config(self):
        with open(self.file_path, 'r') as config_file:
            data = json.load(config_file)
            return GameMode.from_dict(data)

    def save_config(self, config):
        if type(config.theme) is str:
            return
        with open(self.file_path, 'w') as config_file:
            json_obj = json.dumps(config.to_dict())
            config_file.write(json_obj)
