import json
import logging
from pymongo import MongoClient
from bson import ObjectId

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ANSI escape code for red text
RED_TEXT = "\033[91m"
RESET_COLOR = "\033[0m"  # Reset color to default

def log_alert(message):
    return RED_TEXT + message + RESET_COLOR

with open("config.json", "r") as f:
    config = json.load(f)

url = "mongodb://"
url += f'{config["mongodb"]["username"]}:{config["mongodb"]["password"]}'
url += "@"
for server in config["mongodb"]["servers"]:
    url += f"{server},"

url += "/?replicaSet=rs0&readPreference=nearest&authMechanism=DEFAULT"

url = url.replace(",/", "/")

client = MongoClient(url)
db = client['website']

event_role = {}

events = db.events.find()

for event in events:
    logger.info(f"Processing event with _id: {event.get('_id')}")
    for role in event.get("roles"):
        logger.info(f"Role name: {role.get('name')}")
        count = role.get("count")
        logger.debug(f"Current count: {count}")
        db_count = db.signups.count_documents({"event_id": str(event.get("_id")), "roles": {"$in": [role.get("name")]}})
        logger.debug(f"Database count: {db_count}")
        if count != db_count:
            logger.error(log_alert("Database count and count differ!"))
            db.events.update_one({"_id": event.get("_id"), "roles.name": role.get("name")}, {"$set": {"roles.$.count": db_count}})
            logger.info("Updated count in the database.")
