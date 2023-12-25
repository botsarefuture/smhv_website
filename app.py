# Internal imports
<<<<<<< HEAD
from pymongo import DeleteOne
=======
>>>>>>> 4462b321dd4f6ddf900e0b2323c66329b34054b2
from mail import join_email
from well_being import calculate_well_being
from db_utils import *

# Flask related imports
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    Response,
    flash,
    make_response,
    jsonify,
    session,
)
from flask_ckeditor import CKEditor
import werkzeug
from flask_cors import CORS
from flask_sitemap import Sitemap

# MongoDB related imports
from bson import ObjectId

# System imports
import json

from events.email import signup_email

# Date and time related imports
from datetime import datetime
import time
from dateutil import tz
from datetime import datetime


with open("config.json", "r") as f:
    config = json.load(f)


app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config["SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS"] = True
ckeditor = CKEditor(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
sitemap = Sitemap(app=app)


@app.before_request
def set_language():
    supported_languages = ["fi", "en"]
    werkzeug.datastructures.LanguageAccept([(al[0][0:2], al[1]) for al in request.accept_languages]).best_match(supported_languages)
    lang = request.accept_languages.best_match(supported_languages, "en")

    if "user" not in session:
        session["user"] = {
            "lang": lang,
            "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
            "time": datetime.now(),
        }

    if session["user"].get("ip") == "127.0.0.1":
        print(session)


# Function to save answers and well-being score to MongoDB
def save_data(answers, well_being):
    collection = db["well_being_data"]
    data = {"answers": answers, "well_being_score": well_being}
    result = collection.insert_one(data)
    return result.inserted_id


@app.route("/calculate_well_being", methods=["POST"])
def calculate_well_being_api():
    data = request.get_json()
    answers = {
        "anger": data["anger"],
        "anxiety": data["anxiety"],
        "self_harming": data["self_harming"],
        "suicidality": data["suicidality"],
        "tiredness": data["tiredness"],
        "sadness": data["sadness"],
        "happiness": data["happiness"],
        "joy": data["joy"],
        "love": data["love"],
        "crush": data["crush"],
    }

    # Calculate well-being score
    well_being = calculate_well_being(list(answers.values()))

    # Save answers and well-being score to MongoDB
    inserted_id = save_data(answers, well_being)

    response = {
        "well_being_score": well_being,
        "shareable_link": f"/share/{inserted_id}",  # Generate a link with the inserted MongoDB document ID
    }
    return jsonify(response)


# Define a route to share the well-being data
@app.route("/share/<string:document_id>")
def share_well_being(document_id):
    # Retrieve data from MongoDB using the document ID
    collection = db["well_being_data"]
    data = collection.find_one({"_id": ObjectId(document_id)})
    data["_id"] = str(data["_id"])
    return render_template("mental/show.html", data=data)


@app.route("/mental")
def mental():
    return render_template("mental/index.html")


@app.route("/robots.txt", methods=["GET"])
def robots_txt():
    content = "User-agent: *\nDisallow:"
    response = Response(content, content_type="text/plain")
    return response


@app.route("/")
def index():
    lang = session["user"]["lang"]

    return render_template(f"{lang}/index.html", title="")


def get_event_date(event):
    date_str = event["date"]
    return datetime.strptime(date_str, "%d.%m.%Y %H.%M")


def sort_events_by_date(events):
    return sorted(events, key=get_event_date)


@app.route("/events/")
def events():
    lang = session["user"]["lang"]
    # Fetch events from MongoDB
    events_data = events_collection.find()

    # Filter out events with past dates
    current_datetime = datetime.now()
    future_events = [
        event for event in events_data if get_event_date(event) >= current_datetime
    ]
    sorted_events = sort_events_by_date(future_events)
    return render_template(
        f"{lang}/events.html", title="Events", events=sorted_events
    )


@app.route("/events/<event_id>")
def event_details(event_id=None):
    lang = session["user"]["lang"]
    event = events_collection.find_one({"_id": ObjectId(event_id)})

    if not event:
<<<<<<< HEAD
        return render_template("event_not_found.html", lang=lang)

=======
        if lang == "fi":
            flash("Tapahtumaa ei löytynyt.", "warning")

        if lang == "en":
            flash("The event was not found", "warning")


        return redirect("/")
>>>>>>> 4462b321dd4f6ddf900e0b2323c66329b34054b2

    return render_template(f"{lang}/event_details.html", event=event)


@app.route("/signup/<event_id>", methods=["GET", "POST"])
def event_signup(event_id=None):
    lang = session["user"]["lang"]
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
<<<<<<< HEAD
        return render_template("event_not_found.html", lang=lang)

=======
        if lang == "fi":
            flash("Tapahtumaa ei löytynyt.", "warning")

        if lang == "en":
            flash("The event was not found", "warning")


        return redirect("/")
>>>>>>> 4462b321dd4f6ddf900e0b2323c66329b34054b2

    if not event.get("role_signup", False):
        pass

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        roles = request.form.getlist("roles[]")  # Haetaan valitut roolit

        if name == "" or email == "":
            return render_template(
                f"{lang}/signup.html", event_id=event_id, event=event
            )

        roles1 = roles
        # Tallenna ilmoittautumistiedot MongoDB:hen (event_signups-kokoelmaan).
        signup_data = {
            "event_id": event_id,
            "language": lang,
            "name": name,
            "email": email,
            "roles": roles,
        }

        roles = event.get("roles", [])  # Haetaan roolit

        for role in roles:  # ÄLÄ KOSKE
            if role.get("show_name") in roles1:  # ÄLÄ KOSKE!
                # Alusta 'count' rooliin, jos sitä ei ole
                role.setdefault("count", 0)
                # Kasvata roolin 'count' kunkin ilmoittautumisen yhteydessä
                role["count"] += 1

                # Päivitä roolin tiedot tietokantaan käyttäen $inc operaattoria
                events_collection.update_one(
                    {"_id": ObjectId(event_id), "roles.show_name": role["show_name"]},
                    {"$inc": {"roles.$.count": 1}},
                )

        introductions = list()

        for role in roles:
            if role.get("show_name") in roles1:
                if not role.get("introductions") in introductions:
                    introductions += role.get("introductions")

        event["introductions"] = introductions
        # Lisää signup_data MongoDB-kokoelmaan ilmoittautumisia varten.
        result = signups_collection.insert_one(signup_data)
        print(result.inserted_id)
        signup_email(event, {"name": name, "email": email, "roles": roles1}, lang, str(result.inserted_id))

        

        if lang == "fi":
            flash("Ilmoittautuminen onnistui!", "info")

        if lang == "en":
            flash("Successfully registered!", "info")

        # Uudelleenohjaa takaisin tapahtumasivulle ilmoittautumisen jälkeen.
        return redirect(f"/events")
    return render_template(f"{lang}/signup.html", event_id=event_id, event=event)


@app.route("/api/events/")
@app.route("/api/events/<event_id>") # type: ignore
def api_event(event_id=None):
    if event_id != None:
        search = {"_id": ObjectId(event_id)}
        event = db.events.find_one(search)

        event = event
        event["_id"] = str(event["_id"])
        return event

    if event_id == None:
        event = db.events.find()
        # Fetch events from MongoDB
        events_data = events_collection.find()

        # Filter out events with past dates
        current_datetime = datetime.now()
        future_events = [
            event for event in events_data if get_event_date(event) >= current_datetime
        ]
        sorted_events = sort_events_by_date(future_events)
        events = []

        for item in sorted_events:
            item["_id"] = str(item["_id"])
            events.append(item)

        return events


@app.route("/event_watch/")
def event_watch():
    return render_template("thig.html")


@app.route("/participant_remove/<_id>", methods=["GET", "POST"])
def remove_participant(_id):
    lang = session["user"]["lang"]

    if request.method == "GET":
        try:
            event_id = signups_collection.find_one({"_id": ObjectId(_id)}).get("event_id")
            event = events_collection.find_one({"_id": ObjectId(event_id)})

        except:
            return render_template("event_not_found.html", lang=lang)

            

        if event == None:
            return render_template("not_found.html", lang=lang)

        return render_template(f"{lang}/remove_participant.html", _id=_id, event=event)
    
    if request.method == "POST":
        signups_collection.delete_one({"_id": ObjectId(_id)})
        if lang == "en":
            flash("Successfully removed the participation", "info")

        if lang == "fi":
            flash("Ilmoittautuminen poistettu onnistuneesta", "info")
        return redirect("/")
    


# EVENTS END


# @app.route('/<lang>/about')
@app.route("/about")
def about():
    lang = session["user"]["lang"]
    return render_template(f"{lang}/about.html", title="About Us")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    lang = session["user"]["lang"]
    if request.method == "GET":
        return render_template(
            f"{lang}/contact.html", title="Contact Us"
        )

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        phonenumber = request.form.get("phonenumber")

        contactions_collection.insert_one(
            {
                "name": name,
                "email": email,
                "message": message,
                "phonenumber": phonenumber,
            }
        )
        # TODO: #51 Flash information about successfully sent form
        return render_template(
            f"{lang}/contact.html", title="Contact Us"
        )


@app.route("/join", methods=["GET", "POST"])
def join():
    lang = session["user"]["lang"]
    if request.method == "GET":
        return render_template(
            f"{lang}/join_us.html", title="Join Us"
        )

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        phonenumber = request.form.get("phonenumber")
        roles = request.form.getlist("roles")
        join_email({"name": name, "email": email, "roles": roles}, lang)

        joins_collection.insert_one(
            {
                "name": name,
                "email": email,
                "message": message,
                "phonenumber": phonenumber,
                "roles": roles,
            }
        )

        # TODO: #50 Flash information about successfully sent form
        return render_template(
            f"{lang}/join_us.html", title="Join Us"
        )


@app.route("/change_language/<lang>")
def change_language(lang):
    session["user"]["lang"] = lang
    session.modified = True

    if request.referrer and request.referrer.startswith("/change_language/"):
        return redirect("/")

    if request.referrer == None:
        return redirect("/")

    return redirect(request.referrer)


# BLOG
blog_collection = db["blog_posts"]


@app.route("/blog/")
def blog():
    lang = session["user"]["lang"]

    posts = list(blog_collection.find({"lang": lang}))
    return render_template(f"blog/{lang}/blog.html", posts=posts)


@app.route("/blog/<post_id>")
def blog_post(post_id=None):
    lang = session["user"]["lang"]
    post = blog_collection.find_one({"_id": ObjectId(post_id)})
    return render_template(f"blog/{lang}/blog_post.html", post=post)


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    lang = session["user"]["lang"]

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]
        post_data = {
            "title": title,
            "author": author,
            "content": content,
            "lang": lang,
            "date_posted": datetime.now(),
        }
        blog_collection.insert_one(post_data)
        return redirect("/blog")
    return render_template(f"blog/{lang}/create_post.html")


def convert(mongo_db_date):
    # Convert the MongoDB date string to a datetime object
    mongo_date = mongo_db_date  # datetime.fromisoformat(mongo_db_date)

    # Define a function to convert to RFC822 format
    def mongo_to_rfc822(mongo_date):
        # Convert the MongoDB date to UTC timezone
        mongo_date_utc = mongo_date.replace(tzinfo=tz.tzutc())

        # Format it as RFC822 date-time
        rfc822_date = mongo_date_utc.astimezone(tz.tzlocal()).strftime(
            "%a, %d %b %Y %H:%M:%S %z"
        )

        return rfc822_date

    # Call the function to get the RFC822 formatted date
    rfc822_date = mongo_to_rfc822(mongo_date)

    return rfc822_date


@app.route("/rss", methods=["GET"])
def rss_feed():
    # Replace this with your actual blog posts data

    blog_posts = list(blog_collection.find())

    # Create an RSS feed
    rss = f'''<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>Your Blog RSS Feed</title>
            <link>{request.url_root}</link>
            <description>Latest blog posts</description>
            <language>en-us</language>
            <pubDate>{convert(datetime.now())}</pubDate>
            <lastBuildDate>{convert(datetime.now())}</lastBuildDate>
            <docs>https://validator.w3.org/feed/docs/rss2.html</docs>

            {"".join([
                f"""
                <item>
                    <title>{post['title']}</title>
                    <link>{request.url_root}/blog</link>
                    <pubDate>{convert(post['date_posted'])}</pubDate>
                </item>
                """
                for post in blog_posts
            ])}
        </channel>
    </rss>
    '''

    response = make_response(rss)
    response.headers["Content-Type"] = "application/rss+xml"
    return response


# END BLOG


# press releases
press_collection = db["press_releases"]


@app.route("/press")
def press():
    lang = session["user"]["lang"]

    releases = list(press_collection.find())
    print(releases)

    return render_template(f"press/{lang}/press.html", releases=releases)


@app.route("/press/<slug>/")
def press_release(slug=0):
    lang = session["user"]["lang"]

    release = press_collection.find_one({"slug": int(slug)})
    print(release)
    return render_template(f"press/{lang}/press_release.html", release=release)


@app.route("/create_release", methods=["GET", "POST"])
def create_release():
    lang = session["user"]["lang"]

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]
        post_data = {
            "title": title,
            "slug": config["mongodb"]["latest_release"],
            "author": author,
            "content": content,
            "lang": lang,
            "date_released": datetime.now(),
        }
        config["mongodb"]["latest_release"] += 1
        press_collection.insert_one(post_data)
        return redirect("/press")
    return render_template(f"press/{lang}/create_release.html")


@app.route("/toimintaviikko/")
@app.route("/toimintaviikko/info")
@app.route("/api/toimintaviikko/reasons", methods=["GET", "POST"])
def to_main_page(): # THE ACTION WEEK IS OVER, LETS MAKE USER UNABLE TO VISIT IT!
    return redirect("/") # Toimintaviikko is over, so lets just make users unable to visit any page related to it.


release = press_collection.find_one({"slug": 0})
print(release)


@app.route("/contacts")
def contacts():
    lang = session["user"]["lang"]

    return render_template(f"{lang}/contacts.html")

from email_list import add_email, confirm_email
@app.route("/email_list/", methods=["GET", "POST"])
def email_list():
    lang = session["user"]["lang"]

    if request.method == "POST":
        data = request.form
        email_address = data.get('email')
        add_email(email_address, lang) # Add email to database, and also send confirmation email
 
        return render_template(f"{lang}/email/thank_you_join.html")
    
    return render_template(f"{lang}/email/join_email_list.html")
    
    
        
@app.route("/confirm_email/<email_id>")
def confir_email(email_id):
    confirm_email(email_id)
    lang = session["user"]["lang"]
    return render_template(f"{lang}/email/thank_you_confirm.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
