from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash
from app.models import get_db_connection, get_job_details
from flask_login import login_required

bp = Blueprint('jobs', __name__)

@bp.route('/job/<int:id>')
@login_required
def job(id):
    
    selected_job = get_job_details(id)
    user_id = session['user_id']
    res = ''
    with get_db_connection() as conn:
        query = "SELECT 1 FROM registrations WHERE user_id = ? AND job_id = ?"
        result = conn.execute(query, (user_id, id)).fetchone()
        res = result is not None
    return jsonify(selected_job, res)

@bp.route('/api/jobs/<int:id>', methods=['GET'])
@login_required
def jobsSearchMain(id):
    
    conn = get_db_connection()
    jobs = conn.execute("SELECT *  FROM jobsMain").fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs, id= id)

@bp.route('/job/home')
@login_required
def jobs_home():
    
    type = session['type']
    return render_template('jobs_home.html', type=type)

@bp.route('/job')
@login_required
def jobs():
    
    conn = get_db_connection()
    jobs= conn.execute("SELECT * FROM jobsMain").fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs, id = '')