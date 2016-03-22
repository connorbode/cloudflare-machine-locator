from lib import Cloudflare, IPInfo, Settings
from optparse import OptionParser
import sys


def which_from_list(items, message, prop=lambda i: i):
    """
    Asks the user to pick from the list
    """
    choice = None
    while not choice:
        print(message)
        for index, item in enumerate(items):
            title = prop(item)
            print("({}) {}".format(index + 1, title))
        print("~~> ", end="", flush=True)
        read = sys.stdin.readline()
        try:
            num = int(read)
            if num < 1 or num > len(items):
                raise IndexError
            choice = items[num - 1]
        except ValueError:
            print("Sorry, I didn't understand")
        except IndexError:
            print("Sorry, I didn't understand")
    return choice


def get_input(message):
    print(message)
    print("~~> ", end="", flush=True)
    return sys.stdin.readline()[:-1]


def get_action():
    """
    Prompts the user for an action
    """
    actions = [
        {"message": "Add a record", "action": "add_record"},
        {"message": "List zones", "action": "list_zones"},
        {"message": "List DNS records for a zone", "action": "list_dns_records"},
        {"message": "Update records", "action": "update_records"}
    ]
    message = "What would you like to do?"
    prop = lambda a: a['message']
    action = which_from_list(actions, message, prop)
    return action['action']


def list_zones():
    cf.print_zones()


def add_record():
    """
    Adds a DNS record to update to this server
    """
    zones = cf.get_zones()
    message = "Which zone is the DNS record in?"
    prop = lambda z: z['name']
    zone = which_from_list(zones, message, prop)
    message = "Which DNS record would you like to track?"
    records = cf.get_dns_records(zone['id'])
    prop = lambda r: "{} {} -> {}".format(r['type'], r['name'], r['content'])
    record = which_from_list(records, message, prop)
    settings.add_record(zone['id'], record['id'], record['name'])


def generate_settings():
    '''
    Generates a settings file for the application
    '''

    # loop until we get valid credentials
    valid = False
    while not valid:
        email = get_input("What is the email address associated with your Cloudflare account?")
        api_key = get_input("What is your Cloudflare API key?")
        cf = Cloudflare.Cloudflare(email, api_key)
        try:
            cf.get_zones()
            valid = True
        except Cloudflare.CloudflareException:
            print("Cloudflare says your credentials are invalid.")

    # loop until we get valid file
    valid = False
    while not valid:
        try:
            store = get_input("Where would you like to store the settings file?")
            with open(store, 'w') as f:
                Settings.generate(email, api_key, f)
            valid = True
        except Exception as e:
            print(e)
            print("We couldn't write to that file")

    # set the settings for the rest of the program
    options.settings = store


def load_settings():
    if not options.settings:
        actions = [
            {"message": "Generate settings file", "action": "generate_settings"},
            {"message": "Locate settings file", "action": "locate_settings"}
        ]
        prop = lambda a: a['message']
        message = "A settings file was not specified."
        action = which_from_list(actions, message, prop)
        if action['action'] == 'generate_settings':
            generate_settings()
        elif action['action'] == 'locate_settings':
            locate_settings()

parser = OptionParser()
parser.add_option("-s", "--settings",
                  dest="settings", help="path to settings file")
parser.add_option("-a", "--action", dest="action",
                  help="action to perform: list_zones, list_dns_records, update_records")
parser.add_option("-z", "--zone", dest="zone",
                  help="zone id (use action 'list_zones' to find)")

(options, args) = parser.parse_args()

load_settings()

if not options.action:
    print("No action specified.")
    options.action = get_action()

settings = Settings.Settings(options.settings)
cf = Cloudflare.Cloudflare(settings.get_email(), settings.get_api_key())




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
        print(res.status_code)
        print(res.text)

actions = {
    "add_record": add_record,
    "list_zones": list_zones,
    "list_dns_records": list_dns_records,
    "update_records": update_records
}

if options.action not in actions:
    parser.error("action not recognized")

actions[options.action]()
