from db import db

class Student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(50))
    year = db.Column(db.String(10))
    password = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0)
    profile_url = db.Column(db.String(200), default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
    bio = db.Column(db.Text, default="Add your Bio Here")


class Request(db.Model):
    __tablename__ = 'request'
    request_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    learner_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    status = db.Column(db.String(20), default="open")

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'title': self.title,
            'description': self.description,
            'teacher_id': self.teacher_id,
            'learner_id': self.learner_id,
            'status': self.status
        }


class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class StudentSkill(db.Model):
    __tablename__ = 'student_skill'

    student_skill_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id'), nullable=False)
    level = db.Column(db.Enum('beginner', 'intermediate', 'advanced', name='skill_levels'), nullable=False)