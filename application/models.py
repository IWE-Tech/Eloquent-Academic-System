from datetime import datetime
from application import db
from sqlalchemy.orm import relationship

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    studentnumber = db.Column(db.String(20), nullable=False, unique=True)
    gender = db.Column(db.String(5), nullable=False)
    nationality = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    enrolleddate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(30), nullable=False)

    courses = db.relationship('Course', secondary='student_and_class_relation')

class student_and_class_relation(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenumber = db.Column(db.String(10), nullable=False, unique=True)
    coursename = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    credit = db.Column(db.String(5), nullable=False)
    gpa = db.Column(db.String(5), nullable=False)
    location = db.Column(db.String(10), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    students = db.relationship('Student', secondary='student_and_class_relation')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.String(15), nullable=False, unique=True)
    fullname = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(5), nullable=False)
    nationality = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    hire_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)