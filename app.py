from flask import Flask, render_template, request, redirect, make_response
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://95.217.186.200:27017/')
db = client['website']
events_collection = db['events']
visits_collection = db['visits']


def sort_events_by_date(events):
    def get_event_date(event):
        date_str = event['date']
        return datetime.strptime(date_str, '%d.%m.%Y %H.%M')

    return sorted(events, key=get_event_date)


def get_template_folder(lang):
    if lang == 'en':
        return 'en'

    return 'fi'


def set_language_cookie(lang):
    response = make_response(redirect(request.referrer or '/'))
    response.set_cookie('language', lang)
    return response


@app.before_request
def set_template_folder():
    lang = request.cookies.get(
        'language', request.accept_languages.best_match(['fi', 'en']))
    global template_folder
    template_folder = get_template_folder(lang)

    visits_collection.insert_one({"ip": request.headers.get(
        'X-Forwarded-For', request.remote_addr), "lang": lang, "time": datetime.now()})


@app.route("/<lang>/")
@app.route('/')
def index(lang="fi"):
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
    return render_template(f'{lang}/about.html', title='About Us')


@app.route("/<lang>/contact")
@app.route('/contact')
def contact(lang="fi"):
    return render_template(f'{template_folder}/contact.html', title="Contact Us", current_year=2023)


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
