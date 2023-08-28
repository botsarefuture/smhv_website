from flask import Flask, render_template

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


@app.route('/')
def index():
    return render_template('index.html', title="Your Movement Name", current_year=2023)

@app.route('/events')
def events():
    return render_template('events.html', title='Events', events=events_data, current_year=2023)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us", current_year=2023)

if __name__ == '__main__':
    app.run(debug=True)
