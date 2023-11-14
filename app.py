from flask import Flask, request, jsonify, render_template,session,redirect
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shivang123@localhost/sportify'
db = SQLAlchemy(app)
app.secret_key = secrets.token_hex(16)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # sports_preference = db.Column(db.String(255),nullable=False)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            if existing_user.username != data['username']:
                return render_template('login.html', alert_message='Username does not match the provided email.')
            else:
                session['user_id'] = existing_user.id
                return render_template('home.html',user_id=existing_user.id)
        else:
            return render_template('login.html', alert_message='User does not exist')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return render_template('register.html', alert_message='User already exist')
        else:
            new_user = User(email=data['email'], username=data['username'])
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return render_template('home.html',user_id=new_user.id)
    else:
        # Handle GET request for the registration form page here (if needed)
        return render_template('register.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            # Get sports preference from the form data
            sports_preference = request.form.get('sports_preference')
            # Update the sports_preference column in the database
            user.sports_preference = sports_preference

            # Commit the changes to the database
            db.session.commit()

            # Redirect to the profile page after updating preferences
            return redirect('/profile')
        else:
            # Handle case where user does not exist
            pass
    else:
        # Handle case where user is not logged in
        pass



if __name__ == '__main__':
    app.run(debug=True)
