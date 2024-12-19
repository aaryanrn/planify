from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# Create tables
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return render_template('index.html', error='Email already exists')

        new_user = User(name=name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except Exception:
            db.session.rollback()
            return render_template('index.html', error='Registration failed')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error='Invalid credentials')
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('users/dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

# Dummy event data with an ID
events = [
    {"id": 1, "name": "Music Festival", "desc": "Join us for live music and fun!", "image": "event1.jpg"},
    {"id": 2, "name": "Art Exhibition", "desc": "Explore breathtaking artworks.", "image": "event2.jpg"},
    {"id": 3, "name": "Tech Conference", "desc": "Discover the latest in tech innovation.", "image": "event3.jpg"},
    {"id": 4, "name": "Food Carnival", "desc": "Taste delicious food from all around the world.", "image": "event4.jpg"},
    {"id": 5, "name": "Dance Party", "desc": "Dance the night away with great music.", "image": "event5.jpg"},
]

@app.route('/explore-events')
def explore_events():
    return render_template('users/events.html', events=events)

@app.route('/event/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if event:
        return render_template('registration.html', event_name=event['name'], event_id=event_id)
    return redirect('/explore-events')

@app.route('/register_event/<int:event_id>', methods=['POST'])  # Changed route name
def register_event(event_id):
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    # Here you would save this data to a database, send a confirmation email, etc.
    # For now, we'll just print it out.
    print(f"Registered for Event {event_id}: {name}, {email}, {phone}")

    return redirect(url_for('explore_events'))  # Redirect back to the events page


if __name__ == "__main__":
    app.run(debug=True)
