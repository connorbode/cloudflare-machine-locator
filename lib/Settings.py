import json


class Settings:

    def __init__(self, settings_file_path):
        self.settings_file_path = settings_file_path
        settings_file = open(settings_file_path, 'r')
        self.settings = json.load(settings_file)
        settings_file.close()

    def write_settings(self):
        settings_file = open(self.settings_file_path, 'w')
        json.dump(self.settings, settings_file)
        settings_file.close()

    def get_api_key(self):
        return self.settings['api_key']

    def get_email(self):
        return self.settings['email']

    def get_zones(self):
        return self.settings['zones']

    def has_zone(self, zone_id):
        return zone_id in self.settings['zones'].keys()

    def zone_has_record(self, zone_id, record_id):
        zone = self.settings['zones'][zone_id]
        for record in zone:
            if record['id'] == record_id:
                return True
        return False

    def add_record(self, zone_id, record_id, record_name):
        record = {
            'id': record_id,
            'name': record_name
        }

        if self.has_zone(zone_id):
            if self.zone_has_record(zone_id, record_id):
                return
            else:
                self.settings['zones'][zone_id].append(record)
        else:
            self.settings['zones'][zone_id] = [record]
        self.write_settings()
