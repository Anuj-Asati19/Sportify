from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:johncena@localhost/Sportify'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(email=data['email'], username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User registered successfully')
    else:
        # Handle GET request for the registration form page here (if needed)
        return jsonify(message='Invalid request method')


# Additional routes for profile management can be added here
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/sports', methods=['GET'])
def get_sports():
    sports = Sport.query.all()
    sport_list = [{'id': sport.id, 'name': sport.name} for sport in sports]
    return jsonify(sports=sport_list)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    sport_id = db.Column(db.Integer, nullable=False)
    # Add more fields like date, time, location, etc.

@app.route('/create_match', methods=['POST'])
def create_match():
    data = request.get_json()
    new_match = Match(user1_id=data['user1_id'], user2_id=data['user2_id'], sport_id=data['sport_id'])
    db.session.add(new_match)
    db.session.commit()
    return jsonify(message='Match created successfully')

# Additional routes for listing and managing matches can be added here
