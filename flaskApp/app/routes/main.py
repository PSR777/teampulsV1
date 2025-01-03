from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models import get_user_data, get_Percentage, get_db_connection
from app.models import InternshipMain,JobMain, Mentorship, Scholarship, get_internship_details, get_job_details, get_scholarship_details
from flask_login import login_required
bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    
    return render_template('index.html')


@bp.route('/home')
@login_required
def home():
    
    return render_template('home.html')

@bp.route('/profile')
@login_required
def profile():
    
    user_id = session['user_id']
    user_data = get_user_data(user_id)
    if not user_data:
        flash("User data not found.")
        return redirect(url_for('auth.login'))
    filled_percentage = get_Percentage(user_id)
    
    conn = get_db_connection()
    registrations = conn.execute("""
        SELECT internship_id, job_id, scholarship_id FROM registrations WHERE user_id = ?
    """, (user_id,)).fetchall()
    applications = []
    for registration in registrations:
        internship_id, job_id, scholarship_id = registration
        if internship_id:
            internship = get_internship_details(internship_id)
            if internship:
                applications.append({'type': 'internship', 'data': internship})
        if job_id:
            job = get_job_details(job_id)
            if job:
                applications.append({'type': 'job', 'data': job})
        if scholarship_id:
            scholarship = get_scholarship_details(scholarship_id)
            if scholarship:
                applications.append({'type': 'scholarship', 'data': scholarship})
    conn.close()
    
    type = session['type']
    return render_template('profile.html', user=user_data, filled_percentage=filled_percentage, applications=applications, type=type)

@bp.route('/profile/edit')
@login_required
def profile_edit():
    
    user_id = session['user_id']
    user_data = get_user_data(user_id)
    if not user_data:
        flash("User data not found.")
        return redirect(url_for('auth.login'))
    filled_percentage = get_Percentage(user_id)
    return render_template('profile_edit.html', user_data=user_data, filled_percentage=filled_percentage)

@bp.route('/update-user', methods=['POST'])
@login_required
def update_user():
    
    user_id = session['user_id']
    data = request.get_json()
    update_fields = {key: value for key, value in data.items() if value}
    if not update_fields:
        return jsonify({'success': False, 'message': 'No data to update'}), 400
    query = "UPDATE user SET " + ", ".join([f"{key} = ?" for key in update_fields.keys()]) + " WHERE id = ?"
    values = list(update_fields.values()) + [user_id]
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'success': True, 'message': 'User details updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
        
        
        
        
@bp.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')  # Get the search query from the URL parameter

    

    # Perform the search across all tables
    scholarships = Scholarship.query.filter(Scholarship.title.ilike(f'%{query}%')).all()
    mentors = Mentorship.query.filter(Mentorship.name.ilike(f'%{query}%')).all()
    internships = InternshipMain.query.filter(InternshipMain.title.ilike(f'%{query}%')).all()
    jobs = JobMain.query.filter(JobMain.jobTitle.ilike(f'%{query}%')).all()

    # Combine results with their type
    results = [
        {'id': s.id,'title': s.title, 'type': 'Scholarship'} for s in scholarships
    ] + [
        {'id': m.id, 'title': m.name, 'type': 'Mentor'} for m in mentors
    ] + [
        {'id': i.id, 'title': i.title, 'type': 'Internship'} for i in internships
    ] + [
        {'id': j.id, 'title': j.jobTitle, 'type': 'Job'} for j in jobs
    ]
    
    return jsonify(results=results)
    