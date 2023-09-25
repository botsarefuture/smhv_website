from datetime import datetime

from flask import Flask, redirect, render_template, request, Response, flash
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId class
from flask_sitemap import Sitemap
import json

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
sitemap = Sitemap(app=app)

# Set up MongoDB connection
client = MongoClient(config["mongodb"]["uri"])
db = client['website']
events_collection = db['events']
visits_collection = db['visits']
contactions_collection = db['contactions']
joins_collection = db["joins"]
signups_collection = db["signups"]


@app.before_request
def set_template_folder():
    visits_collection.insert_one({"ip": request.headers.get(
        'X-Forwarded-For', request.remote_addr), "lang": "unknown", "time": datetime.now()})

# Serve robots.txt


@app.route('/robots.txt', methods=['GET'])
def robots_txt():
    content = "User-agent: *\nDisallow:"
    response = Response(content, content_type='text/plain')
    return response

@app.route("/<lang>/")
@app.route('/')
def index(lang="fi"):
    if lang == "favicon.ico":
        lang = "fi"

    return render_template(f'{lang}/index.html', title="", current_year=2023)

# EVERYTHING REGARDING EVENTS


def get_event_date(event):
    date_str = event['date']
    return datetime.strptime(date_str, '%d.%m.%Y %H.%M')


def sort_events_by_date(events):
    return sorted(events, key=get_event_date)


@app.route("/<lang>/events")
@app.route('/events')
def events(lang="fi"):
    # Fetch events from MongoDB
    events_data = events_collection.find({"hidden": False}) # If hidden, don't show it!

    # Filter out events with past dates
    current_datetime = datetime.now()
    future_events = [event for event in events_data if get_event_date(
        event) >= current_datetime]
    sorted_events = sort_events_by_date(future_events)
    return render_template(f'{lang}/events.html', title='Events', events=sorted_events, current_year=2023)


@app.route('/<lang>/events/<event_id>')
@app.route('/events/<event_id>')
def event_details(lang="fi", event_id=None):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        # Handle event not found error
        return render_template(f"{lang}/event_not_found.html", current_year=2023)


    return render_template(f'{lang}/event_details.html', event=event, current_year=2023)


@app.route('/<lang>/signup/<event_id>', methods=["GET", "POST"])
@app.route('/signup/<event_id>', methods=["GET", "POST"])
def event_signup(lang="fi", event_id=None):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        # Handle event not found error
        return render_template(f"{lang}/event_not_found.html", current_year=2023)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        roles = request.form.getlist("roles[]")  # Get selected roles

        # Store signup information in MongoDB (event_signups collection).
        signup_data = {
            "event_id": event_id,
            "language": lang,
            "name": name,
            "email": email,
            "roles": roles
        }
        # Insert signup_data into your MongoDB collection for signups.
        signups_collection.insert_one(signup_data)

        if lang == "fi":
            flash("Ilmoittautuminen onnistui!", "info")

        if lang == "en":
            flash("Successfully registered!", "info")
        # Redirect to events page after signup.
        return redirect(f'/{lang}/events')

    return render_template(f'{lang}/signup.html', event_id=event_id, event=event)

# EVENTS END


@app.route('/<lang>/about')
@app.route('/about')
def about(lang="fi"):
    return render_template(f'{lang}/about.html', title='About Us', current_year=2023)


@app.route("/<lang>/contact", methods=["GET", "POST"])
@app.route('/contact', methods=["GET", "POST"])
def contact(lang="fi"):
    if request.method == "GET":
        return render_template(f'{lang}/contact.html', title="Contact Us", current_year=2023)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        phonenumber = request.form.get("phonenumber")

        contactions_collection.insert_one(
            {"name": name, "email": email, "message": message, "phonenumber": phonenumber})
        return render_template(f'{lang}/contact.html', title="Contact Us", current_year=2023)


@app.route("/<lang>/join", methods=["GET", "POST"])
@app.route('/join', methods=["GET", "POST"])
def join(lang="fi"):
    if request.method == "GET":
        return render_template(f'{lang}/join_us.html', title="Join Us", current_year=2023)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        phonenumber = request.form.get("phonenumber")
        roles = request.form.getlist('roles')

        joins_collection.insert_one(
            {"name": name, "email": email, "message": message, "phonenumber": phonenumber, "roles": roles})
        return render_template(f'{lang}/join_us.html', title="Join Us", current_year=2023)

# TODO: #8 Clean this function
def lang_thing(lang, path, request):
    if lang == "fi":
        path = path.replace("en/", "")

    if lang == "en":
        path = path.split("/")        
        
        cont = False
        
        print(request.host_url)
        
        def pop_unne(path, cont):
            for i in range(0, len(path)):
                if cont:
                    continue

                if request.host in path[i]: # Our domain is sinimustaahallitustavastaan.ORG
                    cont = True

                path.pop(i)

        pop_unne(path, cont)

        def list_to_str(listi):
            text = ""
            for item in listi:
                text += f"/{item}"

            text = text.replace("//", "/")

            return text

        path = ("/en/" + list_to_str(path)).replace("//", "/")
        
        path = path.replace("/en/en/", "/en/")

    return path

@app.route('/change_language/<lang>')
def change_language(lang):
    path = lang_thing(lang, request.referrer, request)

    return redirect(path)


if __name__ == '__main__':
    app.run()
