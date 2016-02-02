from lib import Cloudflare, IPInfo, Settings
from optparse import OptionParser
import sys


parser = OptionParser(usage="usage: %prog [options] settings_file")

(options, args) = parser.parse_args()

# verify positional arguments
if len(args) < 1:
    parser.error("wrong number of arguments")

settings_file = args[0]

settings = Settings.Settings(options.settings)
cf = Cloudflare.Cloudflare(settings.get_email(), settings.get_api_key())
ipinfo = IPInfo.IPInfo()
