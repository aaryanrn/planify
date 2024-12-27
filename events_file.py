from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, Event, Registration

# Create Blueprint
events_file = Blueprint('events_file', __name__, template_folder='templates')

# Route: Display all events
@events_file.route('/explore-events')
def explore_events():
    events_list = Event.query.all()  # Fetch events from the database
    return render_template('users/events.html', events=events_list)

# Route: Display event details
@events_file.route('/events_details/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)  # Automatically handles event not found
    return render_template('users/event_details.html', event=event)

@events_file.route('/event_registration/<int:event_id>')
def event_registration_page(event_id):
    event = Event.query.get(event_id)
    if not event:
        flash('Event not found!', 'error')
        return redirect(url_for('events_file.explore_events'))
    return render_template('users/events_registration.html', event=event)

# Route: Register a user to an event
@events_file.route('/register_event', methods=['POST'])
def register_event_user():
    user_id = request.form.get('user_id')
    event_id = request.form.get('event_id')
    remarks = request.form.get('remarks', '')

    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if not user or not event:
        flash('Invalid user or event!', 'error')
        return redirect(url_for('events_file.explore_events'))

    # Create a new registration
    new_registration = Registration(user_id=user_id, event_id=event_id, remarks=remarks)
    db.session.add(new_registration)
    db.session.commit()

    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('events_file.explore_events'))


# Route: Display all registrations
@events_file.route('/registrations', methods=['GET'])
def view_registrations():
    registrations = Registration.query.join(User).join(Event).add_columns(
        User.name, User.email, Event.title, Registration.registration_date, Registration.status
    ).all()
    return render_template('view_registrations.html', registrations=registrations)


# # Route: Register for an event from the event details page
# @events_file.route('/register_event/<int:event_id>', methods=['POST'])
# def register_event(event_id):
#     name = request.form['name']
#     email = request.form['email']
#     phone = request.form['phone']

#     # Validate input
#     if not name or not email or not phone:
#         flash('All fields are required!', 'error')
#         return redirect(url_for('events_file.event_details', event_id=event_id))

#     # Register user (example logic)
#     new_user = User(name=name, email=email, phone_no=phone)
#     db.session.add(new_user)
#     db.session.commit()

#     # Register user for the event
#     new_registration = Registration(user_id=new_user.id, event_id=event_id)
#     db.session.add(new_registration)
#     db.session.commit()

#     flash('Successfully registered for the event!', 'success')
#     return redirect(url_for('events_file.explore_events'))

