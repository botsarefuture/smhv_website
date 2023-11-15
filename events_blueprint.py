# events_blueprint.py

from flask import Blueprint, render_template, redirect, request, flash
from bson import ObjectId
from datetime import datetime
from db_utils import db

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/events')
def events():
    lang = session["user"]["lang"]
    # Fetch events from MongoDB
    events_data = db.events.find()

    # Filter out events with past dates
    current_datetime = datetime.now()
    future_events = [event for event in events_data if get_event_date(event) >= current_datetime]
    sorted_events = sort_events_by_date(future_events)
    return render_template(f'{lang}/events.html', title='Events', events=sorted_events, current_year=2023)

@events_blueprint.route('/events/<event_id>')
def event_details(event_id=None):
    lang = session["user"]["lang"]
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        # Handle event not found error
        pass

    return render_template(f'{lang}/event_details.html', event=event, current_year=2023)

@events_blueprint.route('/signup/<event_id>', methods=["GET", "POST"])
def event_signup(event_id=None):
    lang = session["user"]["lang"]
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        # Handle event not found error
        pass

    if not event.get("role_signup", False):
        pass

    if request.method == "POST":
        # Your signup logic here
        pass

    return render_template(f'{lang}/signup.html', event_id=event_id, event=event)

# Add more routes and functionality related to events as needed

# You can also have a separate file for utility functions like get_event_date, sort_events_by_date, etc.
