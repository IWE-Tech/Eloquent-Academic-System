from flask import render_template, url_for, flash, redirect, request
from application import app, db, bcrypt
from application.models import Course, User, Admin
from application.forms import LoginForm
from flask_login import login_user, current_user, login_required, logout_user



@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    student = 'student'
    teacher = 'teacher'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.id.data).first()                   #query the user from the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):  
            if user.role == teacher:                    #if the user's role is teacher
                login_user(user)
                return redirect(url_for('teacherHome', teacher_name=(user.firstname + user.lastname)))

            elif user.role == student:                  #if the user's role is student
                pass
        else:
            flash('Login failed, please check your id and password', 'danger')

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user
    return redirect(url_for('home'))

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
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        check_user = User.query.filter_by(user_id=id).first()
        if check_user:
            flash('The User is already registered in the system!', 'danger')
            return redirect(url_for('add_user'))
        else:
            user = User(user_id=id, firstname=first, lastname=last, role=role, gender=gender, nationality=nationality, email=email, mobile=mobile, password=hashed_password)
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

#Add the course to the database
#first check if the course isn't already in the system
#If teacher id is specified, check if the teacher is registered in the system
 
    if number and name and time and semester and credit and location:
        course = Course.query.filter_by(coursenumber = number).first()
        if course:
            flash('The course is already in the system', 'danger')
            return redirect(url_for('add_course'))

        if teacher is not '':
            instructor = User.query.filter_by(user_id = teacher).first()
            instructor_role = 'teacher'
            if instructor and instructor.role == instructor_role:
                course = Course(coursenumber=number, coursename=name, time=time, semester=semester, credit=credit, location=location, teacher_id=teacher)
                db.session.add(course)
                db.session.commit()
                flash('The course has been successfully added', 'success')
            else:
                flash('The Teacher is not registered in the system', 'danger')
            return redirect(url_for('add_course'))

        else:
            course = Course(coursenumber=number, coursename=name, time=time, semester=semester, credit=credit, location=location, teacher_id=None)
            db.session.add(course)
            db.session.commit()
            flash('The course has been successfully added', 'success')

    return render_template('/admin/add_course.html')


@app.route('/teacherHome')
@login_required
def teacherHome():
    return render_template('teacher/teacherHome.html', title='TeacherHome')


@app.route('/students')
@login_required
def teacherStudents():
    #course = Course.query.filter_by(Teacher.teacher_id)
    #studentID = student_and_class_relation.query.filter_by(course.coursenumber)
    #student = Student.query.filter_by(studentID.student_id)
    student = User.query.all()
    return render_template('teacher/students.html', title='TeacherStudents', students=student)