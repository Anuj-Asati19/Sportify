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
        data = request.form  # Use request.form to access form data from POST request
        new_user = User(email=data['email'], username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User registered successfully')
    else:
        # Handle GET request for the registration form page here (if needed)
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
