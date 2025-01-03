from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash
from app.models import get_db_connection, get_mentorship_details
from flask_login import login_required

bp = Blueprint('mentorship', __name__)

@bp.route('/mentorship/<int:id>')
@login_required
def mentorship(id):
    
    mentorship = get_mentorship_details(id)
    return jsonify(mentorship)

@bp.route('/api/mentorships/<int:id>')
@login_required
def mentorshipsSearch(id):
    
    conn = get_db_connection()
    mentorships = conn.execute("SELECT *  FROM mentorships").fetchall()
    conn.close()   
    return render_template('mentorship.html', mentorships=mentorships, id = id)

@bp.route('/mentorships')
@login_required
def mentorships():
    
    conn = get_db_connection()
    mentorships = conn.execute("SELECT *  FROM mentorships").fetchall()
    conn.close()   
    return render_template('mentorship.html', mentorships=mentorships, id='')

@bp.route('/mentorship/profile/<string:id>')
@login_required
def mentorship_profile(id):
    
    data = get_mentorship_details(id)
    return render_template('mentorship_profile.html', data=data)