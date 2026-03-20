from flask import Blueprint, request, jsonify, redirect, render_template, flash, url_for
import db from db
import User from models

#define auth blueprint
auth_bp = Blueprint("auth",__name__)

@auth_bp.route('/login',methods=['post'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')
    
@auth_bp.route('/register',methods=['post'])
def register_user():
    username = request.form["uname"]
    email = request.form["email"]
    branch = request.form["branch"]
    year = request.form["year"]

    #find if user exists
    db.execute(f"SELECT * FROM student WHERE email=(%s)",email)
    


