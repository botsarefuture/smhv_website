from pymongo import MongoClient
import json
import os

# Read the MongoDB URI from the config file
with open("config.json", "r") as f:
    config = json.load(f)

global test
test = True

if not test:
    url = config["mongodb"]["url"]

    client = MongoClient(url)
    db = client["website"]
    events_collection = db["events"]


def cont_input(doing) -> bool:
    cont = input(f"Do you want to continue {doing}? (y/n): ").lower().strip() == "y"
    return cont


def fetch_support_role_data(demo_type):
    support_role_folder = "scripts/support role"  # Replace with your folder path
    filename = f"{demo_type}.json"
    file_path = os.path.join(support_role_folder, filename)

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as role_file:
            support_role_data = json.load(role_file)
            return support_role_data
    else:
        print(f"No support role data found for {demo_type}.")
        return None


while True:  # This loop runs indefinitely until manually stopped
    data = {}
    data["title_fi"] = input("The title of the event in Finnish: ")
    data["title_en"] = input("The title of the event in English: ")
    data["date"] = input("The date of the event (DD.MM.YYYY HH.MM): ")
    data["location_fi"] = input("The location of the event in Finnish: ")
    data["location_en"] = input("The location of the event in English: ")
    data["description_fi"] = input("The description of the event in Finnish: ")
    data["description_en"] = input("The description of the event in English: ")
    data["telegram_group"] = input(
        "The link of the telegram group for the support roles: "
    )
    data["role_signup"] = input("The status of signing up for the event? (Y/N)")

    if data["role_signup"].lower() == "y":
        data["role_signup"] = True
    else:
        data["role_signup"] = False

    # Prompt for demonstration type and fetch support role data
    demo_type = input(
        "Enter the type of demonstration [march, roadblock, slow_march, stay_still]: "
    ).lower()
    support_role_data = fetch_support_role_data(demo_type)

    if support_role_data:
        data["roles"] = support_role_data["roles"]

    if not test:
        # Insert the event data into the MongoDB collection
        events_collection.insert_one(data)

    if test:
        print(data)

    if not cont_input("adding another event"):
        break  # Exit the loop if the user does not want to add another event
