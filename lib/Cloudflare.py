import requests


class CloudflareException(Exception):
    pass


class Cloudflare:

    base_url = 'https://api.cloudflare.com/client/v4'

    def __init__(self, email, api_key):
        self.headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': api_key,
            'Content-Type': 'application/json'
        }

    def get(self, path):
        url = "{0}{1}".format(Cloudflare.base_url, path)
        res = requests.get(url, headers=self.headers)
        if res.status_code != 200:
            raise CloudflareException
        return res

    def load_zones(self):
        res = self.get('/zones')
        json = res.json()
        results = json['result']
        self.zones = {}
        for result in results:
            name = result['name']
            self.zones[name] = result

    def list_zone_identifiers(self):
        for name, zone in self.zones.iteritems():
            print("{}: {}".format(name, zone['id']))
