from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from .models import db,User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_mail import Mail, Message
import random



mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    mail = Mail(app)
    from app.routes import auth, main, internships, scholarships, jobs, mentorship, admin, courses,carrier,career_path
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(internships.bp)
    app.register_blueprint(scholarships.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(mentorship.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(carrier.bp)
    app.register_blueprint(career_path.bp)
    

    db.init_app(app)
    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app