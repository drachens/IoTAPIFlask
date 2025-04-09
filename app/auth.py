from flask import Flask
from flask_httpauth import HTTPBasicAuth
from .model import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.checkPassword(password):
        return user

def init_app(app: Flask):
    app.config['SECRET_KEY'] = app.config.get('SECRET_KEY','mysecretkey')
    app.config['BASIC_AUTH_FORCE'] = True