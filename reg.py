from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/sportify'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    sport_id = db.Column(db.Integer, nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify(message='Invalid data'), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(message='User already exists'), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message='User registered successfully')

@app.route('/register', methods=['GET'])
def render_register_page():
    return render_template('register.html')

@app.route('/sports', methods=['GET'])
def get_sports():
    sports = Sport.query.all()
    sport_list = [{'id': sport.id, 'name': sport.name} for sport in sports]
    return jsonify(sports=sport_list)

@app.route('/create_match', methods=['POST'])
def create_match():
    data = request.get_json()
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')
    sport_id = data.get('sport_id')

    if not user1_id or not user2_id or not sport_id:
        return jsonify(message='Invalid data'), 400

    new_match = Match(user1_id=user1_id, user2_id=user2_id, sport_id=sport_id)
    db.session.add(new_match)
    db.session.commit()
    return jsonify(message='Match created successfully')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
