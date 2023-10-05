from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shivang123@localhost/sportify'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            # User with the provided email exists, check if the username matches
            if existing_user.username != data['username']:
                # Username does not match, show an alert
                return render_template('register.html', alert_message='Username does not match the provided email.')
            else:
                # Username matches, log the user in
                return render_template('home.html')
        else:
            # User does not exist, create a new user
            new_user = User(email=data['email'], username=data['username'])
            db.session.add(new_user)
            db.session.commit()
            return render_template('home.html')
    else:
        # Handle GET request for the registration form page here (if needed)
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
