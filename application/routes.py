from flask import render_template, url_for, flash, redirect, request
from application import app
from application.models import Course


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Courses')
def courses():
    courses = Course.query.all()
    return render_template('Courses.html', courses=courses)