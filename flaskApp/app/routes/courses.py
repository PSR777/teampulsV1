from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash, request
from app.models import get_db_connection
from flask_login import login_required
bp = Blueprint('courses', __name__)


@bp.route('/courses')
@login_required 
def courses():
    
    return render_template('courses.html')