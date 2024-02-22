# app/views.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import db, User
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('auth.home'))
        else:
            return render_template('login.html', error = "Invalid username or password")
    return render_template('login.html')

@auth.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username = session['username'])
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error="Username already exists")
    return render_template('register.html')
