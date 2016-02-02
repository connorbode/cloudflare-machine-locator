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
            raise CloudflareException(res)
        return res.json()['result']

    def put(self, path, data):
        url = "{}{}".format(Cloudflare.base_url, path)
        print data
        res = requests.put(url, headers=self.headers, data=data)
        if res.status_code != 200:
            raise CloudflareException(res)
        return res.json()['result']

    def print_zones(self):
        zones = self.get('/zones')
        for zone in zones:
            zone_id = zone['id']
            name = zone['name']
            line = "{} ({})".format(name, zone_id)
            print(line)

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

    def update_records(self, zones, ip):

        for zone, records in zones.iteritems():
            zone_path = '/zones/{}'.format(zone)
            for record in records:

                data = {
                    "type": "A",
                    "content": ip,
                    "id": record
                }

                path = '{}/dns_records/{}'.format(zone_path, record)
                self.put(path, data)
