import subprocess
from datetime import datetime

from flask import Flask, redirect, render_template, request, Response, flash, make_response
from flask_ckeditor import CKEditor

from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId class
from flask_sitemap import Sitemap
import json
from mail import signup_email, join_email
import os
import sys
from datetime import datetime
from dateutil import tz
from flask_cors import CORS

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
sitemap = Sitemap(app=app)
ckeditor = CKEditor(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Set up MongoDB connection
url = "mongodb://"
url += f'{config["mongodb"]["username"]}:{config["mongodb"]["password"]}'
url += "@"
for server in config["mongodb"]["servers"]:
    url += f"{server},"

url += "/?replicaSet=rs0&readPreference=nearest&authMechanism=DEFAULT"

url = url.replace(",/", "/")

client = MongoClient(url)
db = client['website']
events_collection = db['events']
visits_collection = db['visits']
contactions_collection = db['contactions']
joins_collection = db["joins"]
signups_collection = db["signups"]


def restart():

    # Define the command you want to run
    command = "systemctl restart website"

    # Run the command using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with error: {e}")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    except Exception as e:
        print(f"An error occurred: {e}")


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


@app.route("/mongodb/", methods=["POST"])
def mongodb_servers():
    data = request.json
    url = data["url"]
    config["mongodb"]["servers"].append(url)

    with open("config.json", "w") as f:
        json.dump(config, f)

    restart()
    python = sys.executable
    os.execl(python, python, *sys.argv)
    return ""


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
    events_data = events_collection.find()

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
        pass

    return render_template(f'{lang}/event_details.html', event=event, current_year=2023)


@app.route('/<lang>/signup/<event_id>', methods=["GET", "POST"])
@app.route('/signup/<event_id>', methods=["GET", "POST"])
def event_signup(lang="fi", event_id=None):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        # Käsittele tapahtuman puuttumista
        pass

    if not event.get("role_signup", False):
        pass

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        roles = request.form.getlist("roles[]")  # Haetaan valitut roolit

        if name == "" or email == "":
            # Friendly reminder of the fact yu have to provide thights to see
            flash("KYS!", "error")
            return render_template(f'{lang}/signup.html', event_id=event_id, event=event)

        roles1 = roles
        # Tallenna ilmoittautumistiedot MongoDB:hen (event_signups-kokoelmaan).
        signup_data = {
            "event_id": event_id,
            "language": lang,
            "name": name,
            "email": email,
            "roles": roles
        }

        roles = event.get('roles', [])  # Haetaan roolit

        for role in roles:  # ÄLÄ KOSKE
            if role.get("show_name") in roles1:  # ÄLÄ KOSKE!
                # Alusta 'count' rooliin, jos sitä ei ole
                role.setdefault('count', 0)
                # Kasvata roolin 'count' kunkin ilmoittautumisen yhteydessä
                role['count'] += 1

                # Päivitä roolin tiedot tietokantaan käyttäen $inc operaattoria
                events_collection.update_one(
                    {"_id": ObjectId(event_id),
                     "roles.show_name": role["show_name"]},
                    {"$inc": {"roles.$.count": 1}}
                )

        introductions = list()

        for role in roles:
            if role.get("show_name") in roles1:
                if not role.get('introductions') in introductions:
                    introductions += role.get('introductions')

        event["introductions"] = introductions
        signup_email(
            event, {"name": name, "email": email, "roles": roles1}, lang)

        # Lisää signup_data MongoDB-kokoelmaan ilmoittautumisia varten.
        signups_collection.insert_one(signup_data)

        if lang == "fi":
            flash("Ilmoittautuminen onnistui!", "info")

        if lang == "en":
            flash("Successfully registered!", "info")
        # Uudelleenohjaa takaisin tapahtumasivulle ilmoittautumisen jälkeen.
        return redirect(f'/{lang}/events')

    return render_template(f'{lang}/signup.html', event_id=event_id, event=event)


@app.route('/signup1/<event_id>', methods=["GET"])
def event_signup_1(lang="fi", event_id=None):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        return "not"
        pass

    return render_template(f'{lang}/signup1.html', event_id=event_id, event=event)


@app.route("/api/events/")
@app.route("/api/events/<event_id>")
def api_event(event_id=None):
    if event_id != None:
        search = {"_id": ObjectId(event_id)}
        event = db.events.find_one(search)

        event = event
        event["_id"] = str(event["_id"])
        return event

    if event_id == None:
        event = db.events.find()
        events = []

        for item in event:
            item["_id"] = str(item["_id"])
            events.append(item)

        return events


@app.route("/event_watch/")
def event_watch():
    return render_template("thig.html")

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
        # TODO: #51 Flash information about successfully sent form
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
        join_email({"name": name, "email": email, "roles": roles}, lang)

        joins_collection.insert_one(
            {"name": name, "email": email, "message": message, "phonenumber": phonenumber, "roles": roles})

        # TODO: #50 Flash information about successfully sent form
        return render_template(f'{lang}/join_us.html', title="Join Us", current_year=2023)

# TODO: #8 Clean this function


# DO NOT TOUCH THIS! IT'S VERY UNCLEAR WHY THIS WORKS, SO PLS DONT TOUCH THIS!
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

                # Our domain is sinimustaahallitustavastaan.ORG
                if request.host in path[i]:
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


# BLOG
blog_collection = db['blog_posts']


@app.route('/<lang>/blog/')
@app.route('/blog/')
def blog(lang="fi"):
    posts = list(blog_collection.find({"lang": lang}))
    return render_template(f'blog/{lang}/blog.html', posts=posts)


@app.route('/<lang>/blog/<post_id>')
@app.route('/blog/<post_id>')
def blog_post(lang="fi", post_id=None):
    post = blog_collection.find_one({"_id": ObjectId(post_id)})
    return render_template(f'blog/{lang}/blog_post.html', post=post)


@app.route('/<lang>/create_post', methods=['GET', 'POST'])
@app.route('/create_post', methods=['GET', 'POST'])
def create_post(lang="fi"):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        post_data = {
            'title': title,
            'author': author,
            'content': content,
            'lang': lang,
            'date_posted': datetime.now()
        }
        blog_collection.insert_one(post_data)
        return redirect('/blog')
    return render_template(f'blog/{lang}/create_post.html')


def convert(mongo_db_date):
    # Convert the MongoDB date string to a datetime object
    mongo_date = mongo_db_date  # datetime.fromisoformat(mongo_db_date)

    # Define a function to convert to RFC822 format
    def mongo_to_rfc822(mongo_date):
        # Convert the MongoDB date to UTC timezone
        mongo_date_utc = mongo_date.replace(tzinfo=tz.tzutc())

        # Format it as RFC822 date-time
        rfc822_date = mongo_date_utc.astimezone(
            tz.tzlocal()).strftime('%a, %d %b %Y %H:%M:%S %z')

        return rfc822_date

    # Call the function to get the RFC822 formatted date
    rfc822_date = mongo_to_rfc822(mongo_date)

    return rfc822_date


@app.route('/rss', methods=['GET'])
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
press_collection = db['press_releases']


@app.route('/<lang>/press/')
@app.route('/press')
def press(lang="fi"):
    releases = list(press_collection.find())
    print(releases)

    return render_template(f'press/{lang}/press.html', releases=releases)


@app.route('/<lang>/press/<slug>/')
@app.route('/press/<slug>/')
def press_release(lang="fi", slug=0):
    release = press_collection.find_one({'slug': int(slug)})
    print(release)
    return render_template(f'press/{lang}/press_release.html', release=release)


@app.route('/<lang>/create_release', methods=['GET', 'POST'])
@app.route('/create_release', methods=['GET', 'POST'])
def create_release(lang="fi"):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        post_data = {
            'title': title,
            'slug': config["mongodb"]["latest_release"],
            'author': author,
            'content': content,
            'lang': lang,
            'date_released': datetime.now()
        }
        config["mongodb"]["latest_release"] += 1
        press_collection.insert_one(post_data)
        return redirect('/press')
    return render_template(f'press/{lang}/create_release.html')


@app.route("/toimintaviikko/")
def tv():
    return render_template("/toimintaviikko/index.html")


@app.route("/toimintaviikko/info")
def tv_info():
    return render_template("/toimintaviikko/info.html")


release = press_collection.find_one({'slug': 0})
print(release)

app.config["host"] = "sinimustaahallitustavastaan.local"
app.config["port"] = 80
if __name__ == '__main__':
    app.run(port=8000)
