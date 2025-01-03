from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash, request
from app.models import get_db_connection
from flask_login import  login_required, current_user
bp = Blueprint('admin', __name__)

@bp.route('/admin')
@login_required
def admin_dashboard():
    
    if current_user.role != "admin":
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    
    conn = get_db_connection()
    users = conn.execute('SELECT id, User_name, Email, Role FROM user').fetchall()
    internships = conn.execute('SELECT id, company,Title, application_end_date FROM internships_main').fetchall()
    scholarships = conn.execute('SELECT id, Amount,Location, Organization FROM scholarships').fetchall()
    jobs = conn.execute('SELECT id, jobTitle ,salary, companyName FROM jobsMain').fetchall()
    registrations = conn.execute('''
    SELECT 
        registrations.id AS id,
        user.email AS user_email,
        scholarships.title AS scholarship_name,
        jobsMain.jobTitle AS job_name,
        internships_main.title AS internships_name
    FROM 
        registrations
    LEFT JOIN 
        user ON registrations.user_id = user.id
    LEFT JOIN 
        scholarships ON registrations.scholarship_id = scholarships.id
    LEFT JOIN 
        jobsMain ON registrations.job_id = jobsMain.id
    LEFT JOIN 
        internships_main ON registrations.internship_id = internships_main.id
    ''').fetchall()
    conn.close()
    
    jobs_dict = [dict(job) for job in jobs]
    users_dict = [dict(user) for user in users]
    internships_dict = [dict(internship) for internship in internships]
    scholarships_dict = [dict(scholarship) for scholarship in scholarships]
    registrations_dict = [dict(registration) for registration in registrations]
    return render_template('admin.html', users=users_dict, internships=internships_dict, scholarships=scholarships_dict, jobs=jobs_dict, registrations=registrations_dict)

@bp.route('/admin/update', methods=['POST'])
@login_required
def update_record():
    
    if current_user.role != "admin":
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    updated_data = request.get_json()
    table_name = updated_data['header']['table_name']
    id = updated_data['header']['id']
    set_clause = ', '.join([f"{key} = ?" for key in updated_data['column'].keys()])
    values = list(updated_data['column'].values())
    values.append(id)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'UPDATE {table_name} SET {set_clause} WHERE id = ?', values)
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"success": True, "message": f"{table_name.capitalize()} updated successfully"})
        else:
            return jsonify({"success": False, "message": f"{table_name.capitalize()} not found or no changes made"}), 404
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

@bp.route('/admin/delete/<string:type>/<int:id>', methods=['POST'])
@login_required
def delete_record(type, id):
    
    if current_user.role != "admin":
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    table_name = type
    if not table_name:
        return jsonify({"success": False, "message": "Invalid record type"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table_name} WHERE id = ?', (id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"success": True, "message": f"{type.capitalize()} deleted successfully"})
        else:
            return jsonify({"success": False, "message": f"{type.capitalize()} not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()