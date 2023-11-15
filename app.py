from flask import Flask, request, render_template, session, redirect , flash
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shivang123@localhost/sportify'
db = SQLAlchemy(app)
app.secret_key = secrets.token_hex(16)

class NewUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    sports_preference = db.Column(db.String(255), nullable=False)   
    phone_number = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        existing_user = NewUser.query.filter_by(email=data['email']).first()
        if existing_user:
            if existing_user.username != data['username']:
                return render_template('login.html', alert_message='Username does not match the provided email.')
            else:
                session['user_identifier'] = existing_user.email
                return render_template('home.html', user_id=existing_user.id)
        else:
            return render_template('login.html', alert_message='User does not exist')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        existing_user = NewUser.query.filter_by(email=data['email']).first()
        if existing_user:
            return render_template('register.html', alert_message='User already exists')
        else:
            new_user = NewUser(email=data['email'], username=data['username'], sports_preference=data['sport'].lower(), phone_number=data['phone'])
            db.session.add(new_user)
            db.session.commit()
            session['user_identifier'] = new_user.email
            return render_template('home.html', user_id=new_user.id)
    else:
        return render_template('register.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = NewUser.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    user_identifier = session.get('user_identifier')
    if user_identifier:
        user = NewUser.query.filter_by(email=user_identifier).first()
        if user:
            # Get sports preference from the form data
            sports_preference = request.form.get('sports_preferences').lower()
            # Update the sports_preference column in the database
            user.sports_preference = sports_preference

            # Commit the changes to the database
            db.session.commit()
            flash('Preferences updated successfully!', 'success')
            # Redirect to the profile page after updating preferences
            return redirect(f'/profile/{user.id}')
        else:
            # Handle case where user does not exist
            flash('User not found.', 'error')
            pass
    else:
        # Handle case where user is not logged in
        flash('User not logged in.', 'error')
        pass

@app.route('/football_users')
def football_users():
    user_identifier = session.get('user_identifier')
    if user_identifier:
        # Exclude the currently logged-in user
        users = NewUser.query.filter_by(sports_preference='football').filter(NewUser.email != user_identifier).all()
        return render_template('users_list.html', users=users, sport='Football')
    else:
        flash('User not logged in.', 'error')
        return redirect('/')

@app.route('/basketball_users')
def basketball_users():
    user_identifier = session.get('user_identifier')
    if user_identifier:
        # Exclude the currently logged-in user
        users = NewUser.query.filter_by(sports_preference='basketball').filter(NewUser.email != user_identifier).all()
        return render_template('users_list.html', users=users, sport='BasketBall')
    else:
        flash('User not logged in.', 'error')
        return redirect('/')

@app.route('/tennis_users')
def tennis_users():
    user_identifier = session.get('user_identifier')
    if user_identifier:
        # Exclude the currently logged-in user
        users = NewUser.query.filter_by(sports_preference='tennis').filter(NewUser.email != user_identifier).all()
        return render_template('users_list.html', users=users, sport='Tennis')
    else:
        flash('User not logged in.', 'error')
        return redirect('/')

@app.route('/badminton_users')
def badminton_users():
    user_identifier = session.get('user_identifier')
    if user_identifier:
        # Exclude the currently logged-in user
        users = NewUser.query.filter_by(sports_preference='badminton').filter(NewUser.email != user_identifier).all()
        return render_template('users_list.html', users=users, sport='Badminton')
    else:
        flash('User not logged in.', 'error')
        return redirect('/')

@app.route('/swimming_users')
def swimming_users():
    user_identifier = session.get('user_identifier')
    if user_identifier:
        # Exclude the currently logged-in user
        users = NewUser.query.filter_by(sports_preference='swimming').filter(NewUser.email != user_identifier).all()
        return render_template('users_list.html', users=users, sport='Swimming')
    else:
        flash('User not logged in.', 'error')
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
