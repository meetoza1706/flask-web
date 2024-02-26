from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
import datetime 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '1701'
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    # Data = db.relationship('Data', backref='user', lazy=True)

# class Data(db.Model):
#     id = db.Column(db.Integer, Primary_key=True)
#     user_id = db.Column(db.Integer, db.Foreignkey('user.id'), Nullable=False)
#     name =  db.Column(db.String(30), Nullable=False)
#     price = db.Column(db.String(20), Nullable=False)
#     image = db.Column(db.String(100), nullable=True)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('home-logged-in.html')
    else:
        return render_template('home.html')

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
            print("User logged in:", session['logged_in'])
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
    if 'logged_in' in session and session['logged_in']:
        return render_template('contact_us.html')
    else:
        flash('You have not logged in yet', 'danger')
        return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)