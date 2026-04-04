from flask import Blueprint, jsonify, session
from flask import request
from models import Request, Student
from flask import render_template
from db import db

request_bp = Blueprint("request",__name__)

def enrich_request(req):
    teacher = Student.query.get(req.teacher_id)
    learner = Student.query.get(req.learner_id)

    return {
        "request_id": req.request_id,
        "title": req.title,
        "description": req.description,
        "status": req.status,
        "teacher_id": req.teacher_id,
        "learner_id": req.learner_id,
        "teacher_name": teacher.student_name if teacher else "Unknown",
        "learner_name": learner.student_name if learner else "Unknown"
    }


@request_bp.route('/all')
def get_all_requests():
    requests = Request.query.all()
    return jsonify([enrich_request(req) for req in requests])


@request_bp.route('/sent/<user_id>')
def get_sent_requests(user_id):
    requests = Request.query.filter_by(learner_id=user_id).all()
    return jsonify([enrich_request(req) for req in requests])


@request_bp.route('/received/<user_id>')
def get_received_requests(user_id):
    requests = Request.query.filter_by(teacher_id=user_id).all()
    return jsonify([enrich_request(req) for req in requests])

@request_bp.route('/create')
def load_create_request():
    return render_template('createrequest.html')

@request_bp.route('/selected-create')
def load_selected_create_request():
    return render_template('selectedcreaterequest.html')


@request_bp.route('/request/update_status/<int:request_id>', methods=['POST'])
def update_status(request_id):
    data = request.get_json()
    req = Request.query.get(request_id)
    if not req:
        return jsonify({'error': 'Request not found'}), 404
    req.status = data['status']
    db.session.commit()
    return jsonify({'success': True})


# from models import Student

@request_bp.route('/create', methods=['POST'])
def create_request():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    # Get the current user from the database
    user = Student.query.filter_by(email=session['user']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    learner_id = user.student_id
    title = data.get('title')
    description = data.get('description')
    teacher_id = data.get('teacher_id')

    if not teacher_id:
        return jsonify({"error": "Teacher not selected"}), 400

    new_request = Request(
        title=title,
        description=description,
        learner_id=learner_id,
        teacher_id=teacher_id
    )
    db.session.add(new_request)
    db.session.commit()
    db.session.refresh(new_request)
    return jsonify({"message": "Request sent successfully!"})

