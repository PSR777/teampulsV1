import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Sp081698@#$'
    # Add other configuration variables here
    SQLALCHEMY_DATABASE_URI= f'sqlite:///{os.path.join(basedir, "base.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS= True
    MAIL_USERNAME= 'padalasairam777@gmail.com'      # Your email
    MAIL_PASSWORD= 'ezfj szlz snto psun' 