from lib import Cloudflare, IPInfo, Settings
from optparse import OptionParser


parser = OptionParser()
parser.add_option('-s', '--settings', dest='settings',
                  help='Path to the JSON settings file')

(options, args) = parser.parse_args()

settings = Settings.Settings(options.settings)
cf = Cloudflare.Cloudflare(settings.get_email(), settings.get_api_key())
ipinfo = IPInfo.IPInfo()

print "IP: {}".format(ipinfo.get_ip())
print "Zones: {}".format(cf.get_zones())