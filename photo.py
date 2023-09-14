from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, Response
import os

from pymongo import MongoClient

import json

with open("config.json", "r") as f:
    config = json.load(f)


photo_bp = Blueprint('photo', __name__)
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded photos

# Set up MongoDB connection
client = MongoClient(config["mongodb"]["uri"])
db = client['website']

from flask import request, jsonify, Response, flash, redirect, url_for
import os
import json

@photo_bp.route('/upload_photos', methods=['GET', 'POST'])
def upload_photos():
    if request.method == 'POST':
        photos = request.files.getlist('photos[]')
        total_photos = len(photos)
        uploaded_photos = 0

        for photo in photos:
            if photo.filename != '':
                photographer_name = request.form['photographer_name']
                photographer_email = request.form['photographer_email']

                # Save the photo to the specified folder
                photo.save(os.path.join(UPLOAD_FOLDER, photo.filename))

                # Create a MongoDB document for the photo with photographer info
                photo_data = {
                    "filename": photo.filename,
                    "photographer_name": photographer_name,
                    "photographer_email": photographer_email
                }

                # Insert the photo data into MongoDB (you can specify the collection)
                db.photos.insert_one(photo_data)

                uploaded_photos += 1

                # Calculate and send upload progress
                progress = (uploaded_photos / total_photos) * 100
                progress_data = {'progress': progress, 'uploaded': uploaded_photos, 'total': total_photos}
                yield f"data: {json.dumps(progress_data)}\n\n"

        flash('Photos uploaded successfully!', 'success')
        return redirect(url_for('photo.upload_photo'))

    return render_template("photos/upload_photo.html")


@photo_bp.route('/upload_progress')
def upload_progress():
    return Response(generate_progress_updates(), mimetype='text/event-stream')

import time

def generate_progress_updates(total_photos, uploaded_photos):
    # Initialize variables
    progress = 0
    update_interval = 0.5  # Update interval in seconds

    while progress < 100:
        # Calculate progress percentage
        progress = (uploaded_photos / total_photos) * 100

        # Yield progress data as JSON
        yield f"data: {{"progress": {progress}, "uploaded": {uploaded_photos}, "total": {total_photos}}}\n\n"

        # Sleep for a short time to control the update rate
        time.sleep(update_interval)

    # Ensure the progress reaches 100%
    yield f"data: {{"progress": 100, "uploaded": {total_photos}, "total": {total_photos}}}\n\n"



@photo_bp.route('/photo_gallery')
def photo_gallery():
    photos = db.photos.find()
    return render_template('photos/photo_gallery.html', photos=photos)



@photo_bp.route('/download_photo/<filename>')
def download_photo(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
