from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash, request
from app.models import get_db_connection
import requests
bp = Blueprint('career_path', __name__)


@bp.route('/career_path', methods=['POST'])
def career_path():
    data = request.json
    dream_role = data.get('dream_role')
    api_key = 'AIzaSyBTR_KNpqi9rs3HWerW9CRvPRhn8jiEZD0'
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f" my dream role is {dream_role}. Tell me about, what is the job and future growth, demands, avg salary and finally Please suggest a career path and  give me response as good design html tags without headers and body"
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(response)
        print("Response:", response.json())
    else:
        print("Failed to fetch content:", response.status_code, response.text)
    return response.text
