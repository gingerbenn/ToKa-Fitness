from __main__ import app
from flask import url_for, render_template, redirect, request, flash, session, send_from_directory
from db_connector import database
from werkzeug.utils import secure_filename

import hashlib
import requests
import os

db = database()

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/images/profile_pictures')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    title = 'Home'
    current_user = session.get("user")
    return render_template('mainPage.html', title=title, current_user=current_user)


@app.route('/about')
def about():
    title = 'About'
    current_user = session.get("user")
    return render_template('about.html', title=title, current_user=current_user)


@app.route('/profile')
def profile():
    title = "blank"
    current_user = session.get("user")
    return render_template('profile.html', title=title, current_user=current_user)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", '')
    author = request.form.get("author", '')

    db.updateDB("INSERT INTO Books_Table (title,author) VALUES (?,?)", [
                title, author])
    flash("Book added successfully!")

    return redirect(url_for("data"))


@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    book = db.queryDB("SELECT * FROM Books_Table WHERE book_id = ?", [book_id])

    if not book:
        flash('Book not found', 'danger')
    else:
        db.updateDB("DELETE FROM Books_Table WHERE book_id = ?", [book_id])
        flash("Book deleted successfully", "success")

    return redirect(url_for('data'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    title = 'Login'
    current_user = session.get("user")

    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        password = request.form['pword']

        hashed_password = hashlib.md5(str(password).encode()).hexdigest()

        found_user = db.queryDB(
            'SELECT * FROM Customers_Table WHERE name = ?', [user])

        if found_user:
            stored_password = found_user[0][3]

            if stored_password == hashed_password:
                get_user = db.queryDB(
                    'SELECT * FROM Customers_Table WHERE Name = ?', [user])
                session['user'] = get_user
                session['email'] = found_user[0][2]
                flash('Login Successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Try again.', 'danger')
        else:
            flash('User not found. Try again.', 'danger')

    if 'user' in session:
        flash('Already logged in.', 'info')
        return redirect(url_for('about'))
    else:
        return render_template('login.html', current_user=current_user)
    return render_template('login.html', title=title, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Register"
    current_user = session.get("user")

    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pword"]
        email = request.form["email"]
        membership = request.form["mtype"]
        bio = request.form["bio"]
        profile_pic = "default.png"

        hashed_email = hashlib.md5(str(email).encode()).hexdigest()
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()

        result = db.queryDB(
            "SELECT * FROM Customers_Table WHERE Name = ? or Email = ?", [user, hashed_email])
        if result:
            flash("Email or username already exists, please try again.", "danger")
            return redirect(url_for("register"))

        db.updateDB("INSERT INTO Customers_Table (Name, Email, Password, Membership, Bio, Profile_Picture) VALUES (?, ?, ?, ?, ?, ?)", [
                    user, hashed_email, hashed_password, membership, bio, profile_pic])
        return render_template('login.html', current_user=current_user)
    else:
        return render_template("register.html", title=title, current_user=current_user)

    return render_template('register.html', title=title, current_user=current_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user = session.get('user')
            get_user_ID = db.queryDB("SELECT Customer_ID FROM Customers_Table WHERE Name = ?", [user[0][1]])
            filename = str(get_user_ID[0][0]) + "_user_pic"
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+ "/" + filename))

            db.updateDB("UPDATE Customers_Table SET Profile_Picture = ? WHERE Customer_ID = ?", [filename, get_user_ID[0][0]])

            current_user = session.get("user")
            title = "blank"
            flash('Profile Picture has been updated', 'info')
            return render_template('profile.html', title=title, current_user=current_user)

    return render_template('profile.html')


@app.route('/uploads/<name>')
def uploaded_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/logout')
def logout():
    current_user = session.get('user')

    flash('You have been logged out!', 'danger')
    session.pop('user', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('home'))
