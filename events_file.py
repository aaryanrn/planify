from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

# Create Blueprint
events_file = Blueprint('events_file', __name__, template_folder='templates')

# User Table
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    registrations = db.relationship('Registration', backref='user', lazy=True)

# Event Table
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    registrations = db.relationship('Registration', backref='event', lazy=True)

# Registration Table
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # e.g., pending, confirmed, canceled
    remarks = db.Column(db.Text, nullable=True)

# Example route for registering a user to an event
@events_file.route('/register', methods=['POST'])
def register_event_user():
    user_id = request.form.get('user_id')
    event_id = request.form.get('event_id')
    remarks = request.form.get('remarks', '')
    
    user = User.query.get(user_id)
    event = Event.query.get(event_id)
    
    if not user or not event:
        flash('Invalid user or event!', 'error')
        return redirect(url_for('events.explore_events'))
    
    new_registration = Registration(user_id=user_id, event_id=event_id, remarks=remarks)
    db.session.add(new_registration)
    db.session.commit()
    
    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('events.explore_events'))


# Example route to display all registrations
@events_file.route('/registrations', methods=['GET'])
def view_registrations():
    # Fetch all registrations with related user and event data
    registrations = Registration.query.join(User).join(Event).add_columns(User.name, User.email, Event.title, Registration.registration_date, Registration.status)
    return render_template('view_registrations.html', registrations=registrations)


events = [
    {'id': 1, 'name': 'Tech Conference', 'desc': 'A conference about the latest in technology.'},
    {'id': 2, 'name': 'Art Workshop', 'desc': 'Learn advanced art techniques.'},
    {'id': 3, 'name': 'Coding Bootcamp', 'desc': 'Sharpen your coding skills with experts.'},
    {'id': 4, 'name': 'Music Fest', 'desc': 'Enjoy live music from top bands.'},
    {'id': 5, 'name': 'Robotics Expo', 'desc': 'Experience cutting-edge robotics.'},
    {'id': 6, 'name': 'Startup Pitch', 'desc': 'Present your startup idea to investors.'},
    {'id': 7, 'name': 'Fitness Camp', 'desc': 'Get fit with professional trainers.'},
    {'id': 8, 'name': 'Photography Walk', 'desc': 'Learn photography with experts.'}
]

# Route to display all events
@events_file.route('/explore-events')
def explore_events():
    # Fetch all events
    # events_list = Event.query.all()
    events_list=events
    return render_template('users/events.html', events=events_list)


# Route to display event details
# @events.route('/event/<int:event_id>', methods=['GET'])
# def event_details(event_id):
#     event = Event.query.get(event_id)
#     if event:
#         return render_template('registration.html', event_name=event.title, event_id=event_id)
#     return redirect(url_for('events.explore_events'))
@events_file.route('/events_details/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        return render_template('registration.html', event_name=event['name'], event_id=event_id)
    return redirect(url_for('users.explore_events'))

# Register the user for an event (on event details page)
# @events.route('/register_event/<int:event_id>', methods=['POST'])
# def register_event(event_id):
    # Get form data
    # name = request.form['name']
    # email = request.form['email']
    # phone = request.form['phone']
    
    # Create a new user for the registration (this is an example)
    # new_user = User(name=name, email=email, phone_no=phone)
    # db.session.add(new_user)
    # db.session.commit()

    # Register the user for the event
    # new_registration = Registration(user_id=new_user.id, event_id=event_id)
    # db.session.add(new_registration)
    # db.session.commit()

    # flash('Successfully registered for the event!', 'success')
    # return redirect(url_for('events.explore_events'))
    
@events_file.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    # Here you would save this data to a database, send a confirmation email, etc.
    # For now, we'll just print it out.
    print(f"Registered for Event {event_id}: {name}, {email}, {phone}")

    return redirect(url_for('events.explore_events'))  # Redirect back to the events page
