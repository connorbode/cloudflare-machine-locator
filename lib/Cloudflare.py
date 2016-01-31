import requests


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
        return requests.get(url, headers=self.headers)

    def get_zones(self):
        return self.get('/zones')
