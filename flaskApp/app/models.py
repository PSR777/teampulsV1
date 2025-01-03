import sqlite3
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    pronoun = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    work_experience = db.Column(db.String(255))
    current_sector = db.Column(db.String(100))
    current_designation = db.Column(db.String(100))
    organisation_or_college = db.Column(db.String(255))
    location = db.Column(db.String(100))
    DOB = db.Column(db.Date)
    current_address = db.Column(db.Text)
    role = db.Column(db.String(50))
    college = db.Column(db.String(255))
    course = db.Column(db.String(100))
    course_duration = db.Column(db.String(50))
    country = db.Column(db.String(50))
    permanent_address = db.Column(db.Text)
    purpose = db.Column(db.String(255))
    interest_area = db.Column(db.Text)
    skills = db.Column(db.Text)
    certificates = db.Column(db.Text)
    projects = db.Column(db.Text)
    achievements = db.Column(db.Text)
    hobbies = db.Column(db.Text)
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    portfolio = db.Column(db.String(255))

    def __repr__(self):
        return f'<UserProfile {self.user_name}>'
    
class Scholarship(db.Model):
    __tablename__ = 'scholarships'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    type = db.Column(db.String(100))
    location = db.Column(db.String(255))
    amount = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    duration = db.Column(db.String(100))
    applicationFee = db.Column(db.String(100))
    numberAvailable = db.Column(db.Integer)
    requiredDocuments = db.Column(db.Text)
    applicationLink = db.Column(db.String(255))
    contactEmail = db.Column(db.String(120))
    website = db.Column(db.String(255))
    terms_and_conditions = db.Column(db.Text)
    important_dates = db.Column(db.Text)
    additional_benefits = db.Column(db.Text)
    contact_phone = db.Column(db.Float)
    country = db.Column(db.String(100))
    selection_criteria = db.Column(db.Text)
    documents = db.Column(db.Text)

class Mentorship(db.Model):
    __tablename__ = 'mentorships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    rating = db.Column(db.Float)
    experience = db.Column(db.String(255))
    field = db.Column(db.String(100))
    reviews = db.Column(db.Integer)
    organization = db.Column(db.String(255))
    department = db.Column(db.String(100))
    role = db.Column(db.String(100))
    bookings = db.Column(db.Integer)
    mentoringMins = db.Column(db.Integer)
    available = db.Column(db.Boolean)
    isTopMentor = db.Column(db.Boolean)

class JobMain(db.Model):
    __tablename__ = 'jobsMain'
    id = db.Column(db.Integer, primary_key=True)
    companyLogo = db.Column(db.String(255))
    jobTitle = db.Column(db.String(255))
    companyName = db.Column(db.String(255))
    location = db.Column(db.String(255))
    updatedDate = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    impressions = db.Column(db.Integer)
    applicationDeadline = db.Column(db.String(100))
    eligibility = db.Column(db.Text)
    jobSummary = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    qualifications = db.Column(db.Text)
    experienceMin = db.Column(db.Integer)
    experienceMax = db.Column(db.Integer)
    workingDays = db.Column(db.String(100))
    jobType = db.Column(db.String(100))
    jobTiming = db.Column(db.String(100))

class InternshipMain(db.Model):
    __tablename__ = 'internships_main'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    company = db.Column(db.String(255))
    company_logo_text = db.Column(db.String(255))
    location = db.Column(db.String(255))
    duration = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    working_days = db.Column(db.String(100))
    job_type = db.Column(db.String(100))
    experience = db.Column(db.String(255))
    responsibilities = db.Column(db.Text)
    requirements = db.Column(db.Text)
    application_start_date = db.Column(db.String(100))
    application_end_date = db.Column(db.String(100))
    applications_received = db.Column(db.Integer)
    perks = db.Column(db.Text)

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'))
    mentorship_id = db.Column(db.Integer, db.ForeignKey('mentorships.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobsMain.id'))
    internship_id = db.Column(db.Integer, db.ForeignKey('internships_main.id'))
    applied_at = db.Column(db.DateTime, server_default=func.now())
    posted = db.Column(db.String(100))

    user = db.relationship('User', backref=db.backref('registrations', lazy=True))
    scholarship = db.relationship('Scholarship', backref=db.backref('registrations', lazy=True))
    mentorship = db.relationship('Mentorship', backref=db.backref('registrations', lazy=True))
    job = db.relationship('JobMain', backref=db.backref('registrations', lazy=True))
    internship = db.relationship('InternshipMain', backref=db.backref('registrations', lazy=True))
    
    
    
def get_db_connection():
    conn = sqlite3.connect('base.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_data(user_id):
    conn = get_db_connection()
    user_data = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user_data) if user_data else None

def get_Percentage(user_id):
    conn = get_db_connection()
    user_data = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
    columns_info = conn.execute("PRAGMA table_info(user);").fetchall()
    total_columns = len(columns_info)
    filled_count = sum(1 for value in user_data if value is not None and value != '')
    filled_percentage = ' ' + str(int((filled_count / total_columns) * 100)) + '%'
    conn.close()
    return filled_percentage

def get_internship_details(internship_id):
    conn = get_db_connection()
    internship = conn.execute('SELECT * FROM internships_main WHERE id = ?', (internship_id,)).fetchone()
    conn.close()
    if internship:
        return dict(internship)
    return {"error": "Internship not found"}

def get_scholarship_details(scholarship_id):
    conn = get_db_connection()
    scholarship = conn.execute('SELECT * FROM scholarships WHERE id = ?', (scholarship_id,)).fetchone()
    conn.close()
    if scholarship:
        return dict(scholarship)
    return {"error": "Scholarship not found"}

def get_job_details(job_id):
    conn = get_db_connection()
    job = conn.execute('SELECT * FROM jobsMain WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    if job:
        return dict(job)
    return {"error": "Job not found"}

def get_mentorship_details(mentorship_id):
    conn = get_db_connection()
    mentorship = conn.execute('SELECT * FROM mentorships WHERE id = ?', (mentorship_id,)).fetchone()
    conn.close()
    if mentorship:
        return dict(mentorship)
    return {"error": "Mentorship not found"}

def email_exists(email):
    conn = get_db_connection()
    user = conn.execute("SELECT 1 FROM user WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user is not None