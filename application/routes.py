from flask import render_template, url_for, flash, redirect, request
from application import app


@app.route('/')
def home():
    return render_template('home.html')
