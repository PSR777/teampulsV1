from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash, request
from app.models import get_db_connection, get_internship_details
from datetime import datetime
from flask_login import login_required
bp = Blueprint('internships', __name__)

@bp.route('/internship/<int:id>')
@login_required
def internships(id):
    
    selected_internship = get_internship_details(id)
    user_id = session['user_id']
    res = ''
    with get_db_connection() as conn:
        query = "SELECT 1 FROM registrations WHERE user_id = ? AND internship_id = ?"
        result = conn.execute(query, (user_id, id)).fetchone()
        res = result is not None
    return jsonify(selected_internship, res)

@bp.route('/internship/home')
@login_required
def internship_home():
    
    type = session['type']
    return render_template('internship_home.html', type=type)

@bp.route('/internships')
@login_required
def internship():
    
    conn = get_db_connection()
    jobs = conn.execute("SELECT *  FROM internships_main").fetchall()
    conn.close()
    return render_template('internship.html', jobs=jobs, id = '')

@bp.route('/api/internships/<int:id>', methods=['GET'])
@login_required
def internshipSearchMain(id):
    
    conn = get_db_connection()
    jobs = conn.execute("SELECT *  FROM internships_main").fetchall()
    conn.close()
    return render_template('internship.html', jobs=jobs, id= id)

@bp.route('/internship/post', methods=['GET', 'POST'])
@login_required
def internship_post():
    
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        title = request.form.get('title')
        logoUrl2 = request.form.get('logourl')
        organization_name = request.form.get('organization_name')
        status = request.form.get('status')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        registerCount = request.form.get('registerCount')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        duration = request.form.get('duration')
        stipend = request.form.get('stipend')
        posted = datetime.now().date()
        about = request.form.get('about')
        skills = request.form.get('skills')
        certifications = request.form.get('certifications')
        who_can_apply = request.form.get('who_can_apply')
        perks = request.form.get('perks')
        openings = request.form.get('openings')
        logo = request.files['logo'].filename
        cursor.execute('''
            INSERT INTO internships (
                title, logoUrl2, organization_name, status, start_date, end_date, registerCount, 
                location, job_type, duration, stipend, posted, about, skills, certifications, 
                who_can_apply, perks, openings, logo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            title, logoUrl2, organization_name, status, start_date, end_date, registerCount,
            location, job_type, duration, stipend, posted, about, skills, certifications,
            who_can_apply, perks, openings, logo
        ))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    return render_template('internship_post.html')