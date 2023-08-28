from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)

events_data = [
    {
        'title': 'Event 1',
        'date': 'September 10, 2023',
        'location': 'Virtual or Physical Location',
        'description': 'Description of Event 1...'
    },
    {
        'title': 'Event 2',
        'date': 'September 15, 2023',
        'location': 'Virtual or Physical Location',
        'description': 'Description of Event 2...'
    }
    # Add more events
]

def get_template_folder(lang):
    if lang == 'fi':
        return 'fi'
    
    return 'en'

def set_language_cookie(lang):
    response = make_response(redirect(request.referrer or '/'))
    response.set_cookie('language', lang)
    return response

@app.route('/')
def index():
    lang = request.cookies.get('language', request.accept_languages.best_match(['fi', 'en']))
    template_folder = get_template_folder(lang)
    return render_template(f'{template_folder}/index.html', title="Your Movement Name", current_year=2023)

@app.route('/events')
def events():
    lang = request.cookies.get('language', request.accept_languages.best_match(['fi', 'en']))
    template_folder = get_template_folder(lang)
    return render_template(f'{template_folder}/events.html', title='Events', events=events_data, current_year=2023)

@app.route('/about')
def about():
    lang = request.cookies.get('language', request.accept_languages.best_match(['fi', 'en']))
    template_folder = get_template_folder(lang)
    return render_template(f'{template_folder}/about.html', title='About Us')

@app.route('/contact')
def contact():
    lang = request.cookies.get('language', request.accept_languages.best_match(['fi', 'en']))
    template_folder = get_template_folder(lang)
    return render_template(f'{template_folder}/contact.html', title="Contact Us", current_year=2023)

@app.route('/change_language/<lang>')
def change_language(lang):
    return set_language_cookie(lang)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
