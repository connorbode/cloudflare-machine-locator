from lib import Cloudflare, IPInfo, Settings
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-s", "--settings",
                  dest="settings", help="path to settings file")
parser.add_option("-a", "--action", dest="action",
                  help="action to perform: list_zones, list_dns_records, update_records")
parser.add_option("-z", "--zone", dest="zone",
                  help="zone id (use action 'list_zones' to find)")

(options, args) = parser.parse_args()

if not options.settings:
    parser.error("settings file must be specified")

if not options.action:
    parser.error("action must be specified")

settings = Settings.Settings(options.settings)
cf = Cloudflare.Cloudflare(settings.get_email(), settings.get_api_key())


def list_zones():
    cf.print_zones()


def list_dns_records():
    if not options.zone:
        parser.error("zone must be specified")
    cf.print_dns_records(options.zone)


def update_records():
    try:
        ipinfo = IPInfo.IPInfo()
        ip = ipinfo.get_ip()
        cf.update_records(settings.get_zones(), ip)
    except Cloudflare.CloudflareException as ex:
        res = ex.args[0]
        print res.status_code
        print res.text

actions = {
    "list_zones": list_zones,
    "list_dns_records": list_dns_records,
    "update_records": update_records
}

if options.action not in actions:
    parser.error("action not recognized")

actions[options.action]()
