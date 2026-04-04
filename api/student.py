from flask import Blueprint, render_template, redirect, url_for, session, flash
# from functools import wraps
from flask import request, jsonify
import jwt
from models import Student, Request, Skill, StudentSkill
from db import db
# from auth.login import token

student_bp = Blueprint("student", __name__)

@student_bp.route('/dashboard')
def get_dashboard():
    user = Student.query.filter_by(email=session['user']).first()

    if not user:
        return redirect(url_for('auth.login_user'))

    #Sent = user is learner
    sent_requests = Request.query.filter_by(
        learner_id=user.student_id
    ).all()

    #Received = user is teacher
    received_requests = Request.query.filter_by(
        teacher_id=user.student_id
    ).all()

    return render_template(
        'dashboard.html',
        user=user,
        sent_requests=sent_requests,
        received_requests=received_requests
    )


@student_bp.route('/discover')
def get_discover():
    if 'user' not in session:
        return redirect(url_for('auth.login_user'))

    user = Student.query.filter_by(email=session['user']).first()
    return render_template('discover.html', user=user)

@student_bp.route('/discover/users')
def load_all_users():
    if 'user' not in session:
        return redirect(url_for('auth.login_user'))

    users = Student.query.all()
    return jsonify({
    "users": [
        {
            "student_id": user.student_id,
            "student_name": user.student_name,
            "email": user.email,
            "department": user.department,
            "year": user.year,
            "points": user.points,
        }
        for user in users
    ]
})

@student_bp.route('/profile')
def get_profile():
    if 'user' not in session:
        return redirect(url_for('auth.login_user'))

    user = Student.query.filter_by(email=session['user']).first()
    return render_template('profile.html', user=user)

@student_bp.route('/settings')
def get_settings():
    if 'user' not in session:
        return redirect(url_for('auth.login_user'))
    

@student_bp.route('/add-skill', methods=['POST'])
def add_skill():
    if 'user' not in session:
        return redirect(url_for('login_user'))

    student = Student.query.filter_by(email=session['user']).first()

    existing_skill = request.form.get('existing_skill')
    new_skill = request.form.get('new_skill')
    level = request.form.get('level')

    skill_obj = None

    #Case 1: User selected existing skill
    if existing_skill:
        skill_obj = Skill.query.filter_by(name=existing_skill).first()

    # Case 2: User typed new skill
    elif new_skill:
        # Check if already exists (important)
        skill_obj = Skill.query.filter_by(name=new_skill).first()

        if not skill_obj:
            skill_obj = Skill(name=new_skill)
            db.session.add(skill_obj)
            db.session.commit()

    #No skill provided
    else:
        flash("Please select or enter a skill")
        return redirect(url_for('student.get_profile'))

    # Check if already added
    existing_entry = StudentSkill.query.filter_by(
        student_id=student.student_id,
        skill_id=skill_obj.skill_id
    ).first()

    if existing_entry:
        flash("Skill already added")
        return redirect(url_for('student.get_profile'))

    #Add to student_skill table
    student_skill = StudentSkill(
        student_id=student.student_id,
        skill_id=skill_obj.skill_id,
        level=level
    )

    db.session.add(student_skill)
    db.session.commit()

    flash("Skill added successfully")
    return redirect(url_for('student.get_profile'))