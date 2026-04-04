#starter template for a Flask web app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from api.auth import auth_bp
from api.student import student_bp
from api.request import request_bp
import dotenv
import os
from db import db

dotenv.load_dotenv()

app = Flask(__name__)


#configure your app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillsharingplatform.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#set up routes
@app.route('/')
def index():
    return redirect(url_for('auth.login_page'))

app.register_blueprint(auth_bp)
app.register_blueprint(request_bp)
app.register_blueprint(student_bp)

#run your app
if __name__ == '__main__':
    app.run(debug=True)
#TODO: add more routes and functionality as needed, such as editing and deleting requests, user registration, etc.