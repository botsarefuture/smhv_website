from datetime import datetime

from flask import Flask, redirect, render_template, request, Response
from pymongo import MongoClient
from flask_sitemap import Sitemap
import json

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
sitemap = Sitemap(app=app)


# Set up MongoDB connection
if config["mongodb"]["username"] is not None:
    config["mongodb"]["uri"] = f'mongodb://{config["mongodb"]["username"]}:{config["mongodb"]["password"]}@{config["mongodb"]["uri"].replace("mongodb://", "")}'
    
client = MongoClient(config["mongodb"]["uri"])
db = client['website']
events_collection = db['events']
visits_collection = db['visits']
contactions_collection = db['contactions']
joins_collection = db["joins"]

def sort_events_by_date(events):
    def get_event_date(event):
        date_str = event['date']
        return datetime.strptime(date_str, '%d.%m.%Y %H.%M')

    return sorted(events, key=get_event_date)


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


@app.route("/<lang>/events")
@app.route('/events')
def events(lang="fi"):
    # Fetch events from MongoDB
    events_data = events_collection.find()
    sorted_events = sort_events_by_date(events_data)

    return render_template(f'{lang}/events.html', title='Events', events=sorted_events, current_year=2023)


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
        
        contactions_collection.insert_one({"name": name, "email": email, "message": message, "phonenumber": phonenumber})
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
        
        joins_collection.insert_one({"name": name, "email": email, "message": message, "phonenumber": phonenumber, "roles": roles})
        return render_template(f'{lang}/join_us.html', title="Join Us", current_year=2023)
    

@app.route('/change_language/<lang>')
def change_language(lang):
    if lang == "en":
        path = request.referrer.split("/")[-1]
        path = "/en/" + path

    if lang == "fi":
        path = request.referrer.replace("/en/", "/")

    return redirect(path)


if __name__ == '__main__':
    app.run()
