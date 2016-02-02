from lib import Cloudflare, IPInfo, Settings
from optparse import OptionParser


parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-s", "--settings",
                  dest="settings", help="path to settings file")
parser.add_option("-a", "--action", dest="action",
                  help="action to perform: list_zones, update_records")

(options, args) = parser.parse_args()

if not options.settings:
    parser.error("settings file must be specified")

if not options.action:
    parser.error("action must be specified")

settings = Settings.Settings(options.settings)
cf = Cloudflare.Cloudflare(settings.get_email(), settings.get_api_key())


def list_zones():
    cf.load_zones()
    cf.list_zone_identifiers()


def update_records():
    pass

actions = {
    "list_zones": list_zones,
    "update_records": update_records
}

if options.action not in actions:
    parser.error("action not recognized")

actions[options.action]()
