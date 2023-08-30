from flask import Flask, render_template, request, redirect, make_response
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://95.217.186.200:27017/')
db = client['website']
events_collection = db['events']
visits_collection = db['visits']

def get_template_folder(lang):
    if lang == 'fi':
        return 'fi'

    return 'en'

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

    visits_collection.insert_one({"ip": request.remote_addr, "lang": lang, "time": datetime.now()})

@app.route('/')
def index():
    return render_template(f'{template_folder}/index.html', title="Your Movement Name", current_year=2023)


@app.route('/events')
def events():
    # Fetch events from MongoDB
    events_data = events_collection.find()
    return render_template(f'{template_folder}/events.html', title='Events', events=events_data, current_year=2023)


@app.route('/about')
def about():
    return render_template(f'{template_folder}/about.html', title='About Us')


@app.route('/contact')
def contact():
    return render_template(f'{template_folder}/contact.html', title="Contact Us", current_year=2023)


@app.route('/change_language/<lang>')
def change_language(lang):
    return set_language_cookie(lang)


if __name__ == '__main__':
    app.run()
