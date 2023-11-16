import json
import logging
from pymongo import MongoClient
from bson import ObjectId
import time

# Configure the logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ANSI escape code for red text
RED_TEXT = "\033[91m"
RESET_COLOR = "\033[0m"  # Reset color to default


def log_alert(message):
    return RED_TEXT + message + RESET_COLOR


with open("../config.json", "r") as f:
    config = json.load(f)

url = config["mongodb"]["url"]

client = MongoClient(url)
db = client["website"]

event_role = {}

events = db.events.find()

for event in events:
    logger.info(f"Processing event with _id: {event.get('_id')}")
    print(event.get("title_fi"))
    count_full = 0

    email_signup_mapping = {}  # Dictionary to map emails to signups

    for role in event.get("roles"):
        logger.info(f"Role name: {role.get('name')}")
        count = role.get("count")
        logger.debug(f"Current count: {count}")

        # Get all signups for this event and role
        signups = db.signups.find(
            {
                "event_id": str(event.get("_id")),
                "roles": {
                    "$elemMatch": {"$in": [role.get("name"), role.get("show_name")]}
                },
            }
        )

        for signup in signups:
            # Check if the email already exists in the mapping
            email = signup.get("email")
            if email in email_signup_mapping:
                if email_signup_mapping[email]["_id"] == signup["_id"]:
                    continue

                # If the email exists, update the existing signup with the new role
                existing_signup = email_signup_mapping[email]

                if not role.get("name") in existing_signup["roles"]:
                    existing_signup["roles"].append(role.get("name"))

                # Update the existing signup in the database
                db.signups.update_one(
                    {"_id": existing_signup["_id"]},
                    {"$set": {"roles": existing_signup["roles"]}},
                )
                # Notify of the update
                logger.info("Updated existing signup in the database.")

                # Remove the current signup
                db.signups.delete_one({"_id": signup["_id"]})
                # Notify of the deletion
                logger.info("Deleted the current signup.")
            else:
                # If the email doesn't exist, add a new entry in the mapping
                email_signup_mapping[email] = signup

        logger.info(f"Role name: {role.get('name')}")
        count = role.get("count")
        logger.debug(f"Current count: {count}")
        db_count = db.signups.count_documents(
            {
                "event_id": str(event.get("_id")),
                "roles": {
                    "$elemMatch": {"$in": [role.get("name"), role.get("show_name")]}
                },
            }
        )
        logger.debug(f"Database count: {db_count}")
        if count != db_count:
            logger.error(log_alert("Database count and count differ!"))
            db.events.update_one(
                {"_id": event.get("_id"), "roles.name": role.get("name")},
                {"$set": {"roles.$.count": db_count}},
            )
            # Notify of the update
            logger.info("Updated count in the database.")
        if db_count != 0:
            print(role.get("name"), db_count)

    count_1 = db.signups.count_documents({"event_id": str(event.get("_id"))})
    print(f"For event {event.get('title_fi')}: {count_1}")
