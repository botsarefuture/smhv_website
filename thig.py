import requests

# Define the API endpoint
api_url = "http://127.0.0.1/api/events/"

# Make a GET request to the API
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    events = response.json()

    # Iterate through each event
    for event in events:
        # Extract event details
        title_fi = event.get("title_fi")
        title_en = event.get("title_en")
        date = event.get("date")
        location_fi = event.get("location_fi")
        location_en = event.get("location_en")
        description_fi = event.get("description_fi")
        description_en = event.get("description_en")
        telegram_group = event.get("telegram_group")

        print(f"Title (FI): {title_fi}")
        print(f"Title (EN): {title_en}")
        print(f"Date: {date}")
        print(f"Location (FI): {location_fi}")
        print(f"Location (EN): {location_en}")
        print(f"Description (FI): {description_fi}")
        print(f"Description (EN): {description_en}")
        print(f"Telegram Group: {telegram_group}")

        # Handle roles
        roles = event.get("roles")
        if roles:
            for role in roles:
                role_name = role.get("name")
                show_name = role.get("show_name")
                fi_name = role.get("fi_name")
                en_name = role.get("en_name")
                fi_description = role.get("fi_description")
                en_description = role.get("en_description")
                min_count = role.get("min_count")
                count = role.get("count")

                print(f"Role Name: {role_name} ({show_name})")
                print(f"Role Name (FI): {fi_name}")
                print(f"Role Name (EN): {en_name}")
                print(f"Role Description (FI): {fi_description}")
                print(f"Role Description (EN): {en_description}")
                print(f"Minimum Count: {min_count}")
                print(f"Count: {count}")
                print("------")  # Separation between roles

        print("======================================")  # Separation between events

else:
    print(f"Failed to fetch events. Status Code: {response.status_code}")
