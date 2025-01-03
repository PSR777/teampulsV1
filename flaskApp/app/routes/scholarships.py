from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash, request
from app.models import get_db_connection, get_scholarship_details
from flask_login import login_required

bp = Blueprint('scholarships', __name__)

@bp.route('/scholarship/<int:id>')
@login_required
def scholarship(id):
    
    
    scholarship = get_scholarship_details(id)
    user_id = session['user_id']
    res = ''
    with get_db_connection() as conn:
        query = "SELECT 1 FROM registrations WHERE user_id = ? AND scholarship_id = ?"
        result = conn.execute(query, (user_id, id)).fetchone()
        res = result is not None
    return jsonify(scholarship, res)

@bp.route('/scholarship/home')
@login_required
def scholarship_home():
    
    type = session['type']
    return render_template('scholarship_home.html', type=type)

@bp.route('/api/scholarships/<int:id>')
@login_required
def scholarshipsSearch(id):
    
    conn = get_db_connection()
    scholarships = conn.execute("SELECT * FROM scholarships").fetchall()
    conn.close()
    return render_template('scholarship.html', scholarships=scholarships, id = id)

@bp.route('/scholarships')
@login_required
def scholarships():
    
    conn = get_db_connection()
    scholarships = conn.execute("SELECT * FROM scholarships").fetchall()
    conn.close()
    return render_template('scholarship.html', scholarships=scholarships, id= '')

@bp.route('/scholarship/post', methods=['GET', 'POST'])
@login_required
def scholarship_post():
    
    if request.method == 'POST':
        data = request.get_json()
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO scholarships (documents, additional_benefits, amount, applicationFee, applicationLink,
                                    contactEmail, deadline, description, duration, eligibility, important_dates,
                                    numberAvailable, organization, selection_criteria, terms_and_conditions, 
                                    title, type, website, location, contact_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (data.get('Documents'), data.get('additionalBenefits'), data.get('amount'), data.get('applicationFee'),
                      data.get('applicationLink'), data.get('contactEmail'), data.get('deadline'), data.get('description'),
                      data.get('duration'), data.get('eligibility'), data.get('importantDates'), data.get('numberAvailable'),
                      data.get('organization'), data.get('selectionProcess'), data.get('termsConditions'), data.get('title'),
                      data.get('type'), data.get('website'), data.get('location'), data.get('contactPhone')))
            conn.commit()
        except Exception as e:
            print("Error inserting data:", e)
        finally:
            conn.close()
        return jsonify({"message": "Scholarship added successfully!"}), 201
    return render_template('scholarship_post.html')