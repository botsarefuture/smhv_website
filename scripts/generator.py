from pymongo import MongoClient
import json

# Read the MongoDB URI from the config file
with open("config.json", "r") as f:
    config = json.load(f)

global test
test = True

if not test:
    # Set up MongoDB connection
    client = MongoClient(config["mongodb"]["uri"])
    db = client["website"]
    events_collection = db["events"]


def cont_input(doing) -> bool:
    cont = input(f"Do you want to continue {doing}? (y/n): ").lower().strip() == "y"
    return cont


while True:  # This loop runs indefinitely until manually stopped
    data = {}
    data["title_fi"] = input("The title of the event in Finnish: ")
    data["title_en"] = input("The title of the event in English: ")
    data["date"] = input("The date of the event (DD.MM.YYYY HH.MM): ")
    data["location_fi"] = input("The location of the event in Finnish: ")
    data["location_en"] = input("The location of the event in English: ")
    data["description_fi"] = input("The description of the event in Finnish: ")
    data["description_en"] = input("The description of the event in English: ")
    data["roles"] = []

    to_continue = True

    while to_continue:
        role = {}
        role["name"] = input("The name of the role: ").replace(" ", "")
        role["show_name"] = input("The show name of the role: ")
        role["fi_name"] = input("The name of the role in Finnish: ")
        role["en_name"] = input("The name of the role in English: ")
        role["fi_description"] = input("The description of the role in Finnish: ")
        role["en_description"] = input("The description of the role in English: ")

        introductions = []
        intro_continue = True

        while intro_continue:
            introduction = {
                "date": input("The date of introduction (DD.MM.YYYY): "),
                "time": input("Time of introduction (hh.mm): "),
                "location": input("The location of introduction: "),
            }
            introductions.append(introduction)
            intro_continue = cont_input("creating introductions")

        role["introductions"] = introductions
        data["roles"].append(role)
        to_continue = cont_input("creating roles")

    if not test:
        # Insert the event data into the MongoDB collection
        events_collection.insert_one(data)

    if test:
        print(json.dumps(data))

    if not cont_input("adding another event"):
        break  # Exit the loop if the user does not want to add another event
