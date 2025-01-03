from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash, request
from app.models import get_db_connection
from flask_login import  login_required
bp = Blueprint('carrier', __name__)


@bp.route('/carrier')
@login_required 
def carrier():
    
    conn = get_db_connection()
    mentorships = conn.execute("SELECT *  FROM mentorships").fetchall()   
    conn.close() 
    conn = get_db_connection()
    scholarships = conn.execute("SELECT * FROM scholarships").fetchall()
    conn.close()
    return render_template('carrier.html', mentorships = mentorships, scholarships = scholarships)