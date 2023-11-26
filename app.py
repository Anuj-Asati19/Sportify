from flask import Flask, request, render_template, session, redirect , flash, url_for
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
                return redirect(url_for('home', user_id=existing_user.id))
                # return render_template('home.html', user_id=existing_user.id)
        else:
            return render_template('login.html', alert_message='User does not exist')
    else:
        return render_template('login.html')
    
@app.route('/home/<int:user_id>', methods=['GET'])
def home(user_id):
    messages=[]
    if user_id in notifications.keys():
        messages=reversed(notifications[user_id])
    else:
        messages.append("No new message")
    return render_template('home.html', user_id=user_id, message_list=messages)

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
            return redirect(url_for('home', user_id=new_user.id))

    else:
        return render_template('register.html')

@app.route('/profile/<int:user_id>', methods=['GET'])
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


@app.route('/sport/<int:user_id>', methods=['GET'])
def sport(user_id):
    sport_name = request.args.get('name')  
    print(sport_name)
    user_identifier = session.get('user_identifier')
    if user_identifier:
        # users = NewUser.query.filter_by(sports_preference=sport_name).filter(NewUser.email != user_identifier).all()
        return redirect(url_for('users_list',user_id=user_id,user_identifier=user_identifier,sport=sport_name))
    else:
        return redirect(url_for('index'))


notifications = {} 

def add_notification(target_user_id, sender_user, ground_selection,sport):
    sender_name=NewUser.query.get(sender_user).username
    notification_message = f"{sender_name} sent a request for {ground_selection} to play {sport}"
    if target_user_id in notifications:
        notifications[target_user_id].append(notification_message)
    else:
        notifications[target_user_id] = [notification_message]


@app.route('/send_request', methods=['POST','GET'])
def send_request():
    ground_selection = request.form.get('ground_selection')
    user_id = request.form.get('user_id', type=int)
    sport = request.form.get('sport')
    sender_user_id = request.form.get('sender_id')
    add_notification(target_user_id=user_id, sender_user=sender_user_id, ground_selection=ground_selection,sport=sport)
    
    flash('Request sent successfully!', 'success')
    # users = NewUser.query.filter_by(sports_preference=sport).filter(NewUser.email != user_identifier).all()
    return redirect(url_for('home', user_id=sender_user_id))

    


@app.route('/users_list/<int:user_id>', methods=['GET'])
def users_list(user_id):
    user_identifier=request.args.get('user_identifier')
    print(user_identifier)
    sport=request.args.get('sport')
    print(type(sport))
    users = NewUser.query.filter_by(sports_preference=sport).filter(NewUser.email != user_identifier).all()
    print(users,sport)
    return render_template('users_list.html',users=users, sport=sport, curr_usr_id=user_id)




if __name__ == '__main__':
    app.run(debug=True)
