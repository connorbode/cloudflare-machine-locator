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
        return res.json()['result']

    def load_zones(self):
        results = self.get('/zones')
        self.zones = {}
        for result in results:
            name = result['name']
            self.zones[name] = result

    def list_zone_identifiers(self):
        for name, zone in self.zones.iteritems():
            print("{}: {}".format(name, zone['id']))

    def print_dns_records(self, zone):
        url = '/zones/{}/dns_records'.format(zone)
        records = self.get(url)
        for record in records:
            dns_type = record['type']
            name = record['name']
            ip = record['content']
            dns_id = record['id']
            line = "{} {} -> {} ({})".format(dns_type, name, ip, dns_id)
            print(line)
