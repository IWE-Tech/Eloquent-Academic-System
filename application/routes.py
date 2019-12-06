from flask import render_template, url_for, flash, redirect, request
from application import app, db
from application.models import Course, User, Admin


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('Courses.html', courses=courses)


@app.route('/admn')
def admin():
    return render_template('admin/admin_home.html')

@app.route('/admn/students', methods=['GET', 'POST'])
def students():
    students = User.query.filter_by(role='student')
    return render_template('/admin/students.html', students=students)

@app.route('/admn/teachers', methods=['GET', 'POST'])
def teachers():
    teachers = User.query.filter_by(role='teacher')
    return render_template('/admin/teachers.html', teachers=teachers)

@app.route('/admn/courses', methods=['GET', 'POST'])
def admin_courses():
    courses = Course.query.all()
    return render_template('/admin/courses.html', courses=courses)

@app.route('/admn/add_user', methods=['GET', 'POST'])
def add_user():
    id = request.form.get("id")
    first = request.form.get("firstname")
    last = request.form.get("lastname")
    role = request.form.get("role")
    gender = request.form.get("gender")
    nationality = request.form.get("nationality")
    email = request.form.get("email")
    mobile = request.form.get("mobile")
    password = request.form.get("password")

    if id and first and last and role and gender and nationality and email and mobile and password:
        user = User(user_id=id, firstname=first, lastname=last, role=role, gender=gender, nationality=nationality, email=email, mobile=mobile, password=password)
        db.session.add(user)
        db.session.commit()
        flash('The new user has been added successfully', 'success')
        return redirect(url_for('add_user'))

    return render_template('/admin/add_user.html')

@app.route('/admn/add_course', methods=['GET', 'POST'])
def add_course():
    number = request.form.get("number")
    name = request.form.get("name")
    time = request.form.get("time")
    semester = request.form.get("semester")
    credit = request.form.get("credit")
    location = request.form.get("location")
    teacher = request.form.get("teacher")

    if number and name and time and semester and credit and location:
        course = Course(coursenumber=number, coursename=name, time=time, semester=semester, credit=credit, location=location, teacher_id=teacher)
        db.session.add(course)
        db.session.commit()
        flash('The course has been successfully added', 'success')
        return redirect(url_for('add_course'))
    return render_template('/admin/add_course.html')