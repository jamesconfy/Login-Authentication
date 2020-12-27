from flask import Flask, request, render_template, url_for, session, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import *
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any random string' #must be set to use sessions
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def home_page():
    if 'user_id' in session:
        user_id = session['user_id']
        
        db = DB()

        data = db.GetByID(user_id[0])
        return render_template('viewprofile.html', data=data)
    else:
        return render_template('home_page.html')

@app.route('/signup')
def sign_up():
    return render_template('sign_up.html')

@app.route('/create_profile', methods=['POST'])
def create_profile():
    db = DB()

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    phone_no = request.form['phone_no']

    check_username = db.GetByUsername(username)
    if check_username != None:
        flash('Username Already Exists')
        return redirect(url_for('sign_up'))
    else:
        db.CreateProfile(username, generate_password_hash(password), email, first_name, last_name, dob, address, city, state, phone_no)
        return redirect(url_for('login'))
 
@app.route('/login_page')
def login():
    return render_template('login_page.html')

@app.route('/signin', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        db = DB()

        username = request.form['username']
        password = request.form['password']

        hashed_pass = db.GetPasswordByUsername(username)
        if hashed_pass!=None:
            if check_password_hash(hashed_pass[0], password)==True:
                user_id = db.GetIDBy_Username_Password(username)
                session['user_id'] = user_id

                data = db.GetByID(user_id[0])
                return render_template('viewprofile.html', data=data)
                    
        else:
            flash("Username or Password Incorrect", "info")
            return redirect(url_for('login'))
            

@app.route('/delete_profile')
def delete_profile():
    db = DB()
    id = request.args["id"]

    db.DeleteProfileByID(id)
    return redirect(url_for('home_page'))

@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
    db = DB()
    id = request.args["id"]

    data = db.GetByID(id)
    return render_template('update_profile.html', data=data)

@app.route('/update', methods=['POST', 'GET'])
def update_all():
    db = DB()
    
    id = request.args["id"]
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    phone_no = request.form['phone_no']
    
    db.UpdateAll(id, username, password, email, first_name, last_name, dob, address, city, state, phone_no)

    data = db.GetByID(id)
    return render_template('viewprofile.html', data=data)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        
        flash('You have logout successfully')
        return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)