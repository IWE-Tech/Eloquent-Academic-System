from datetime import datetime
from application import db
from sqlalchemy.orm import relationship

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(20), primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(5), nullable=False)
    nationality = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    courses = db.relationship('Course', backref='teacher')

class SelectedCourses(db.Model):
    __tablename__ = 'selected_courses'
    student_id = db.Column(db.String(20), db.ForeignKey('user.user_id'), primary_key=True)
    course_number = db.Column(db.String(10), db.ForeignKey('course.coursenumber'), primary_key=True)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    coursenumber = db.Column(db.String(10), nullable=False, unique=True)
    coursename = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    credit = db.Column(db.String(5), nullable=False)
    location = db.Column(db.String(10), nullable=False)
    teacher_id = db.Column(db.String(20), db.ForeignKey('user.user_id'), nullable=True)

