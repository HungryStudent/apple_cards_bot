import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
TOKEN = config["settings"]["token"]
API_TOKEN = config["settings"]["API_TOKEN"]
ADMINS = config["settings"]["admins"].split(",")
ADMINS = [int(admin) for admin in ADMINS]
manager_id = config["settings"]["manager"]
notify_url = config["settings"]["notify_url"]
