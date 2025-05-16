from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    default_posts = [  
        {
            'title': 'Bay Street Run Club',
            'city': 'Toronto',
            'image_url': 'https://runningmagazine.ca/wp-content/uploads/2019/09/A59U5465-1024x683.jpg',
            'data': 'Join us every Thursday at 6:15 PM for a 5k run through downtown.',
            'website': 'https://baystreetrun.club',
            'user_id': -1  
        },
        {
            'title': 'Art of Mobility Run Club',
            'city': 'Missisauga',
            'image_url': 'https://runningmagazine.ca/wp-content/uploads/2019/09/A59U4458-1024x683.jpg',
            'data': 'Morning runs every Sunday at 8 AM!',
            'website': 'https://artofmobility.com/services/running-physio/running-club-mississauga/',
            'user_id': -1
        },
    ]
        
    if request.method == 'POST':
        title = request.form.get('title')
        city = request.form.get('city')
        image_url = request.form.get('image_url')
        note = request.form.get('note')
        website = request.form.get('website')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(title=title, data=note, image_url=image_url, city=city, website=website, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Post added!', category='success')
            
        
    search_city = request.args.get('q')
    if search_city:
        notes = Note.query.filter(Note.city.ilike(f"%{search_city}%")).order_by(Note.date.desc()).all()
        filtered_default_posts = [post for post in default_posts if search_city.lower() in post['city'].lower()]
    else:
        notes = Note.query.order_by(Note.date.desc()).all()
        filtered_default_posts = default_posts

    return render_template("home.html", user=current_user, notes=notes + filtered_default_posts)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})