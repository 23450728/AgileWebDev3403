from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')