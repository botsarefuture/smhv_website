from pymongo import MongoClient
import json
import os

# Read the MongoDB URI from the config file
with open("config.json", "r") as f:
    config = json.load(f)

global test
test = False

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


dates = [
    "27.11.2023 16.00",
    "28.11.2023 18.00",
    "29.11.2023 18.00",
    "30.11.2023 18.00",
    "1.12.2023 16.00",
    "2.12.2023 12.00",
    "3.12.2023 13.30",
]

for date in dates:
    data = {}
    data["title_fi"] = "Hidas marssi sinimustaa hallitusta vastaan"
    data["title_en"] = "Slow march against the far-right government"
    data["date"] = date
    data["location_fi"] = (
        "Helsingin keskustan läheisyydessä. Tarkempi sijainti lähetetään osallistujille."
    )
    data["location_en"] = (
        "Near the centre of Helsinki. The exact location will be sent to the participants."
    )
    data["description_fi"] = (
        "Marssitaan yhdessä hallitus alas. Marssi tulee kulkemaan todella hitaasti."
    )
    data["description_en"] = (
        "Let's march together to bring down the government. The march will be moving very slow."
    )
    data["telegram_group"] = "https://t.me/+jU_h00_v1Z1lODU0"
    data["role_signup"] = "Y"

    if data["role_signup"].lower() == "y":
        data["role_signup"] = True
    else:
        data["role_signup"] = False

    # Prompt for demonstration type and fetch support role data
    demo_type = "slow_march"
    support_role_data = fetch_support_role_data(demo_type)

    if support_role_data:
        data["roles"] = support_role_data["roles"]

    if not test:
        # Insert the event data into the MongoDB collection
        events_collection.insert_one(data)
        print(data)

    if test:
        print(data)
