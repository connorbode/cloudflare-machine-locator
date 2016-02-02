import json


class Settings:

    def __init__(self, settings_file_path):
        settings_file = open(settings_file_path, 'r')
        self.settings = json.load(settings_file)

    def get_api_key(self):
        return self.settings['api_key']

    def get_email(self):
        return self.settings['email']

    def get_zones(self):
        return self.settings['zones']

