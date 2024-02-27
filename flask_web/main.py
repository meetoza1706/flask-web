from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '1701'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    Data = db.relationship('Data', backref='user', lazy=True)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    bhk = db.Column(db.String(6), nullable=True)
    location = db.Column(db.String(100), nullable=True)   
    status = db.Column(db.String(50), nullable=True)   
    address = db.Column(db.String(600), nullable=True)   
    floor = db.Column(db.String(10), nullable=True)   
    ownership_type = db.Column(db.String(20), nullable=True)   
    facing_direction = db.Column(db.String(10), nullable=True)
    age_of_construction = db.Column(db.String(10), nullable=True)   
    booking_amount = db.Column(db.String(20), nullable=True)   
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['GET', 'POST'])
def home():
    current_username = None
    print("Session contents:", session)
    
    if 'username' in session:
        current_username = session['username']
        print("Current username:", current_username)

    if 'logged_in' in session and session['logged_in']:
        return render_template('home-logged-in.html', current_username=current_username)
    else:
        return render_template('home.html', current_username=current_username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        print(username, hashed_password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()    
        
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash('Incorrect password or username', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/check_user', methods=['GET', 'POST'])
def check_user():
    if 'logged_in' in session:
        print("User logged in:", session['logged_in'])
        return "user logged in"
    else:
        print("User is not logged in")
        return "no user logged in"
    
@app.route('/contact_us')
def contact_us():
    current_username = None
    print("Session contents:", session)
    
    if 'username' in session:
        current_username = session['username']
        print("Current username:", current_username)
        
    if 'logged_in' in session and session['logged_in']:
        return render_template('contact_us.html')
    else:
        flash('You have not logged in yet', 'danger')
        return render_template('login.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            
            user_id = session.get('user_id')

            name = request.form['name']
            price = request.form['price']
            image = request.files['image']
            bhk = request.form['bhk']
            location = request.form['location']
            status = request.form['status']
            address = request.form['address']
            floor = request.form['floor']
            ownership_type = request.form['ownership_type']
            facing_direction = request.form['facing_direction']
            age_of_construction = request.form['age_of_construction']
            booking_amount = request.form['booking_amount']

            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            
            new_data = Data(user_id=user_id, name=name, price=price, image=filename, bhk=bhk, location=location, status=status, address=address, floor=floor, ownership_type=ownership_type, facing_direction=facing_direction, age_of_construction=age_of_construction, booking_amount=booking_amount)

            db.session.add(new_data)
            db.session.commit()

        return render_template('upload.html')
    else:
        flash('You have not logged in yet', 'danger')
        return render_template('login.html')
    
@app.route('/property', methods=['GET', 'POST'])
def property():
    property_data = Data.query.all()

    return render_template('property.html', property_list=property_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)