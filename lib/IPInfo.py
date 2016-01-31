import requests
import re


class IPInfo:
    def get_ip(self):
        res = requests.get('https://ipinfo.io/ip')
        match = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', res.text)
        return match.group(0)