from datetime import datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/index')
@app.route('/')
@login_required
def index():
    user = {"username": "supratim"}
    posts = [
        {"author": {"username": "Jimmy Carter"},
         "body": "I got the lemon pie"},
        {"author": {"username": "Jimmy Krugel"},
         "body": "I got the apple pie"}
        ]
    return render_template("index.html", title='Home', user=user, posts=posts)


# When you want to interchange data with users, then you need both get and post
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for user {} and remember me {}'.format(form.username.data, form.remember_me.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Username {} does not exist or password is wrong!'.format(form.username.data))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats you are now officially registered as a new user')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


# invoking dynamic content with user profiles
@ app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


