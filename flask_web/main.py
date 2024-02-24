# # from flask import Flask, render_template, request, redirect, url_for, session
# # from flask_sqlalchemy import SQLAlchemy
# # from datetime import datetime
# # from werkzeug.utils import secure_filename
# # import os


# # app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# # app.config['UPLOAD_FOLDER'] = 'static/uploads'
# # app.config['SECRET_KEY'] = '1701'
# # db = SQLAlchemy(app)

# # # Define User and Data models
# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(50), unique=True, nullable=False)
# #     password = db.Column(db.String(100), nullable=False)
# #     data = db.relationship('Data', backref='user', lazy=True)

# # class Data(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Define foreign key
# #     title = db.Column(db.String(100), nullable=False)
# #     desc = db.Column(db.Text, nullable=False)
# #     images = db.relationship('ImageData', backref='data', lazy=True)
# #     date_created = db.Column(db.DateTime, default=datetime.utcnow)


# # class ImageData(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)
# #     filename = db.Column(db.String(100), nullable=False)

# # # Home page route
# # @app.route('/')
# # def home():
# #     return render_template('upload.html')

# # # Login route
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         user = User.query.filter_by(username=username, password=password).first()
# #         if user:
# #             session['user_id'] = user.id
# #             session['username'] = user.username  # Store username in session
# #             return redirect(url_for('upload'))
# #         else:
# #             return "Invalid username or password"
# #     return render_template('login.html')

# # # Registration route
# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         new_user = User(username=username, password=password)
# #         db.session.add(new_user)
# #         db.session.commit()
# #         return redirect(url_for('login'))
# #     return render_template('register.html')

# # # Upload route
# # @app.route('/upload', methods=['POST'])
# # def upload():
# #     if 'user_id' not in session:
# #         return redirect(url_for('login'))  # Redirect to login page if user is not logged in

# #     if request.method == 'POST':
# #         title = request.form['title']
# #         desc = request.form['desc']
        
# #         # Check if the POST request has the file part
# #         if 'images' not in request.files:
# #             return "No file part"
        
# #         images = request.files.getlist('images')  # Get list of uploaded images

# #         # Save each uploaded image to the 'uploads' folder and collect filenames
# #         image_data_list = []  # List to store ImageData objects
# #         for image in images:
# #             if image.filename == '':
# #                 return "No selected file"
# #             if image:
# #                 filename = secure_filename(image.filename)
# #                 image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
# #                 # Save filename of uploaded image to the database
# #                 new_image_data = ImageData(data_id=None, filename=filename)
# #                 db.session.add(new_image_data)
# #                 image_data_list.append(new_image_data)

# #         # Save data entry to the database (title, desc)
# #         new_data = Data(user_id=session['user_id'], title=title, desc=desc)
# #         db.session.add(new_data)
        
# #         # Assign data_id to each ImageData object and commit changes
# #         for image_data in image_data_list:
# #             image_data.data_id = new_data.id
# #         db.session.commit()

# #         return "Data uploaded successfully!"




# # # Route to view uploaded data
# # @app.route('/view_data')
# # def view_data():
# #     if 'user_id' not in session:
# #         return redirect(url_for('login'))  # Redirect to login page if user is not logged in

# #     # Retrieve data entries associated with the logged-in user
# #     user_id = session['user_id']
# #     data_entries = Data.query.filter_by(user_id=user_id).all()

# #     return render_template('view_data.html', data_entries=data_entries)



# # # Logout route
# # @app.route('/logout')
# # def logout():
# #     session.pop('user_id', None)
# #     return redirect(url_for('login'))

# # if __name__ == '__main__':
# #     with app.app_context():
# #         db.create_all()
# #     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from werkzeug.utils import secure_filename
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# app.config['SECRET_KEY'] = '1701'
# db = SQLAlchemy(app)

# # Define User and Data models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     data = db.relationship('Data', backref='user', lazy=True)

# class Data(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     title = db.Column(db.String(100), nullable=False)
#     desc = db.Column(db.Text, nullable=False)
#     images = db.relationship('ImageData', backref='data', lazy=True)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

# class ImageData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)
#     filename = db.Column(db.String(100), nullable=False)

# # Home page route
# @app.route('/')
# def home():
#     return render_template('upload.html')

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username, password=password).first()
#         if user:
#             session['user_id'] = user.id
#             session['username'] = user.username
#             return redirect(url_for('upload'))
#         else:
#             return "Invalid username or password"
#     return render_template('login.html')

# # Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         new_user = User(username=username, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html')

# # Upload route
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():

#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         title = request.form['title']
#         desc = request.form['desc']
        
#         # Check if the POST request has the file part
#         if 'images' not in request.files:
#             return "No file part"
        
#         images = request.files.getlist('images')

#         # Save each uploaded image to the 'uploads' folder and collect filenames
#         image_data_list = []
#         for image in images:
#             if image.filename == '':
#                 return "No selected file"
#             if image:
#                 filename = secure_filename(image.filename)
#                 image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
#                 # Save filename of uploaded image to the database
#                 new_image_data = ImageData(data_id=None, filename=filename)
#                 db.session.add(new_image_data)
#                 image_data_list.append(new_image_data)

#         # Save data entry to the database
#         new_data = Data(user_id=session['user_id'], title=title, desc=desc)
#         db.session.add(new_data)
        
#         # Assign data_id to each ImageData object and commit changes
#         for image_data in image_data_list:
#             image_data.data_id = new_data.id
#         db.session.commit()


#         return render_template('upload.html')
#         return "Data uploaded successfully!"

# # Route to view uploaded data
# @app.route('/view_data')
# def view_data():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     user_id = session['user_id']
#     data_entries = Data.query.filter_by(user_id=user_id).all()

#     return render_template('view_data.html', data_entries=data_entries)

# # Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime 

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, Primary_key = True)
#     username = db.Column(db.String(10), Unique=True, Nullable=False)
#     password = db.Column(db.String(8), Nullable=False)
#     Data = db.relationship('Data', backref='user', lazy=True)

# class Data(db.Model):
#     id = db.Column(db.Integer, Primary_key=True)
#     user_id = db.Column(db.Integer, db.Foreignkey('user.id'), Nullable=False)
#     name =  db.Column(db.String(30), Nullable=False)
#     price = db.Column(db.String(20), Nullable=False)
#     images = db.relationship('ImageData', backref='data', lazy=True)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

# class ImageData(db.Model):
#     id = db.column(db.Integer, Primary_key = True)
#     data_id = db.relationship(db.Integer, db.Foreignkey('data.id'), nullable=False)
#     filename = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return "Welcome to login"

if __name__ == '__main__':
    app.run(debug=True)