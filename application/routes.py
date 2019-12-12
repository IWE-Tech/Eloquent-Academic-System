from flask import render_template, url_for, flash, redirect, request
from application import app, db, bcrypt
from application.models import Course, User, Admin, SelectedCourses
from application.forms import LoginForm
from sqlalchemy import func, and_
from datetime import date
from flask_login import login_user, current_user, login_required, logout_user



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/MyCourses')
def my_courses():
    my_courses = Course.query.join(SelectedCourses, Course.coursenumber == SelectedCourses.course_number).filter_by(student_id=current_user.user_id).all()
    return render_template('student/my_courses.html', my_courses=my_courses,
    SelectedCourses=SelectedCourses, func=func, db=db)

@app.route('/course_selection', methods=['GET', 'POST'])
def courses_selection():
    courses = Course.query.all()
    return render_template('student/Courses.html', courses=courses, date=date)

@app.route('/Course/<string:course_number>/Select', methods=['GET', 'POST'])
def select_course(course_number):
    result = SelectedCourses.query.filter(and_(SelectedCourses.student_id == current_user.user_id,
    SelectedCourses.course_number==course_number)).first()
    
    if result:
        flash('You have already selected this course', 'info')
        return redirect(url_for('courses_selection'))
    else:
        this_course = Course.query.filter_by(coursenumber=course_number).first()
        course = SelectedCourses(student_id=current_user.user_id,
        course_number=course_number, course_time=this_course.time,
        course_credit=this_course.credit)
        #                                  ***
        # we have to check if this student have or not a class at the time of this course before he/she select
        c_with_st = SelectedCourses.query.filter(and_(SelectedCourses.student_id == current_user.user_id,
        SelectedCourses.course_time == this_course.time)).first()
        total_credit = db.session.query(func.sum(SelectedCourses.course_credit)).filter(SelectedCourses.student_id ==
        current_user.user_id).scalar()
        student_courses = SelectedCourses.query.filter_by(student_id=current_user.user_id).all()
        if student_courses and int(total_credit) + int(this_course.credit) > 25:
            flash('You have reached maximum semester credits!', 'warning')
            return redirect(url_for('courses_selection'))
        if c_with_st:
            flash('You have another class at this time!', 'danger')
            return redirect(url_for('courses_selection'))
        else:
            db.session.add(course)
            db.session.commit()
            flash('Successfully selected', 'success')
            return redirect(url_for('courses_selection'))

@app.route('/Course/<string:course_number>/drop', methods=['GET', 'POST'])
def drop_course(course_number):
    result = SelectedCourses.query.filter(and_(SelectedCourses.student_id == current_user.user_id,
    SelectedCourses.course_number==course_number)).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        flash('Successfully droped', 'success')
        return redirect(url_for('my_courses'))
    else:
        flash('You did not selected this course yet', 'info')
        return redirect(url_for('my_courses'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    student = 'student'
    teacher = 'teacher'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.id.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):  
            if user.role == 'teacher':                    #if the user's role is teacher
                login_user(user)
                return redirect(url_for('teacherHome', teacher_name=(user.firstname + user.lastname)))

            elif user.role == 'student':                  #if the user's role is student
                login_user(user)
                return redirect(url_for('my_courses'))
            else:
                flash('Unknown error occured')
                return redirect(url_for('home'))
        else:
            flash('Login failed, please check your id and password', 'danger')

    return render_template('login.html', form = form)

@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.password==form.password.data:
            return redirect(url_for('admin'))
        else:
            flash('Invalid Login details! Try again.', 'danger')

    return render_template('/admin/admin_login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
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

@app.route('/teachercourse', methods=['GET', 'POST'])
def teacher_get_course():
    course = Course.query.filter_by(teacher_id=current_user.user_id).all()
    return redirect(url_for('teacherStudents', course=course))

@app.route('/teachercourse/select', methods=['GET', 'POST'])
def teacher_get_studentid():
    selectSC = SelectedCourses.query.all()
    return redirect(url_for('teacherStudents', select=selectSC))

@app.route('/teachercourse/student', methods=['GET', 'POST'])
def teacher_get_students():
    student = User.query.filter_by(role='student').all()
    return redirect(url_for('teacherStudents', student=student))


@app.route('/courses')
@login_required
def teacherCourse():

    course = Course.query.filter_by(teacher_id=current_user.user_id).all()

    return render_template('teacher/courses.html', title='TeacherCourses', course=course)

@app.route('/teacherevents')
@login_required
def teacherEvents():
    return render_template('teacher/teacherevents.html', title='Events')

@app.route('/teacherschedule')
@login_required
def teacherSchedule():
    course = Course.query.filter_by(teacher_id=current_user.user_id)
    return render_template('teacher/teacherschedule.html', title='Schedule', course=course)

@app.route('/students')
@login_required
def teacherStudents():
    return render_template('teacher/students.html', title='Students')