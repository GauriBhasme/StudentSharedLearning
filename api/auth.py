from flask import Blueprint, request, jsonify, redirect, render_template, flash, url_for, session
# from app import db
from models import Student
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import jwt
import os
import dotenv
from datetime import datetime, timedelta

departments = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL', 'IT', 'BIO-TECH', 'CHEMICAL', 'MCA', 'MBA', 'MSC', 'BSC', 'B.TECH', 'PHD']
years = ['1', '2', '3', '4', '5']

dotenv.load_dotenv()

#define auth blueprint
auth_bp = Blueprint("auth",__name__)

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html', departments=departments, years=years)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    student_name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')
    year = request.form.get('year')
    password = request.form.get('password')

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create user object
    new_student = Student(
        student_name=student_name,
        email=email,
        department=department,
        year=year,
        password=hashed_password
    )

    try:
        db.session.add(new_student)
        db.session.commit()
        flash("Registration Successful!", "success")
        print("New student registered: {}".format(email))
        return redirect(url_for('auth.login_page'))
    except:
        flash("Email already exists!", "error")
        print("Registration failed for email: {}".format(email))
        return redirect(url_for('auth.login_page'))

#LOGIN
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    student = Student.query.filter_by(email=email).first()

    if student and check_password_hash(student.password, password):
        session['user'] = email   # store user in session
        return redirect(url_for('student.get_dashboard'))

    return "Invalid credentials", 401


@auth_bp.route('/logout')
def logout():
    return "Logout successful"

@auth_bp.route('/getuser/<int:user_id>')
def get_user(user_id):
    student = Student.query.get(user_id)
    if student:
        return jsonify({"name": student.student_name})
    else:
        return jsonify({"name": "Unknown"})