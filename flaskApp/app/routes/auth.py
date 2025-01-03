from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from app.models import get_db_connection, email_exists, User, InternshipMain
import hashlib
from datetime import datetime
from flask_login import  login_user, login_required, logout_user, current_user 
import random
from flask_mail import  Message
from app import mail
bp = Blueprint('auth', __name__)


@bp.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    
    # Check if an OTP was already sent to this email in the session
    if session.get('otpEmail') == email:
        return jsonify({'message': 'OTP already sent to this email!'}), 200

    otp = random.randint(100000, 999999)
    
    
    session['otpEmail'] = email
    session['otp'] = otp
    msg = Message('Your OTP Code', sender='padalasairam777@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}'
    mail.send(msg)

    return jsonify({'message': 'OTP sent successfully!'}), 200


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['Password'].encode()).hexdigest()
        otp = request.form['otp']
        print(session['otp'])
        print(session['otpEmail'])
        #if  str(session['otp']) != otp :
        #    return render_template('login.html', error='Invalid otp. Please try again.', email = email, password = request.form['Password'] )
        
        user1 = User.query.filter_by(email=email).first()

        if user1:
            login_user(user1)
            
        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM user WHERE email = ? AND password = ?", (email, password)
            ).fetchone()
        if user:
            session.update({'user_id': user['id'], 'user_name': user['user_name'], 'type': user['user_type']})
            session['otp'] = ''
            session['otpEmail'] = ''
            return redirect(url_for('main.home'))
        return render_template('login.html', error='Invalid credentials. Please try again.', email = email, password = request.form['Password'], otp = otp)
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'user_type': request.form.get('user_type', ''),
            'first_name': request.form.get('First_name', ''),
            'last_name': request.form.get('Last_name', ''),
            'user_name': request.form.get('User_name', ''),
            'email': request.form.get('email', ''),
            'phone_number': request.form.get('Phone_number', ''),
            'password': hashlib.sha256(request.form.get('Password', '').encode()).hexdigest(),
            'college': request.form.get('college', ''),
            'course': request.form.get('course', ''),
            'course_duration': request.form.get('course_duration', ''),
            'dob': request.form.get('dob', ''),
            'current_address': request.form.get('current_address', ''),
            'permanent_address': request.form.get('permanent_address', ''),
            'purpose': request.form.get('purpose', ''),
            'interest_area': request.form.get('interest_area', ''),
            'skills': request.form.get('skills', ''),
            'work_experience': request.form.get('work_experience', ''),
            'certificates': request.form.get('certificates', ''),
            'projects': request.form.get('projects', ''),
            'achievements': request.form.get('achievements', ''),
            'hobbies': request.form.get('hobbies', ''),
            'linkedin': request.form.get('linkedin', ''),
            'github': request.form.get('github', ''),
            'twitter': request.form.get('twitter', ''),
            'portfolio': request.form.get('portfolio', '')
        }
        
        if email_exists(user_data['email']):
            flash("User with this email already exists. Please log in using the link below.")
            return redirect(url_for('auth.login'))
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user (user_type, first_name, last_name, user_name, email, phone_number, password, 
                                college, course, course_duration, dob, current_address, permanent_address, 
                                purpose, interest_area, skills, work_experience, certificates, projects, 
                                achievements, hobbies, linkedin, github, twitter, portfolio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(user_data.values()))
            conn.commit()
            session.update({'user_id': cursor.lastrowid, 'user_name': user_data['user_name']})
        
        return redirect(url_for('main.home'))
    
    return render_template('signup.html')

@bp.route('/check-email')
def check_email():
    email = request.args.get('email')
    return jsonify({"exists": email_exists(email)})

@bp.route('/logout')
def logout():
    logout_user()
    
    flash("You have been logged out.")
    return redirect(url_for('auth.login'))

@bp.route('/test')
@login_required  
def test():
    internship = InternshipMain.query.get(1)
    print(internship.title )
    return render_template('home2.html')