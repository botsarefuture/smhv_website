# MongoDB related imports
from pymongo import MongoClient
from bson import ObjectId

# System imports
import json

with open("config.json", "r") as f:
    config = json.load(f)

client = MongoClient(config["mongodb"].get("url"))
db = client["website"]
events_collection = db["events"]
visits_collection = db["visits"]
contactions_collection = db["contactions"]
joins_collection = db["joins"]
signups_collection = db["signups"]
