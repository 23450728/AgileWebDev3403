from flask import render_template, flash, redirect, url_for, request, g, send_from_directory
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post, Comment, Image
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
import os

@app.before_request
def before_request():
    g.search_form = SearchForm()

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.id.desc())
    posts = db.paginate(query, page=page, per_page=4, error_out=False)
    imageQuery = sa.select(Image).order_by(Image.id.desc())
    images = db.paginate(imageQuery, page=page, per_page=4, error_out=False)
    return render_template("home.html", posts=posts.items, images=images.items)

@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.id.desc())
    posts = db.paginate(query, page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    imageQuery = sa.select(Image).order_by(Image.post_id.desc())
    images = db.paginate(imageQuery, page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", posts=posts.items, images=images.items, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit() 
        if form.file.data.filename != "":
            filename = str(post.id) + '.png'
            form.file.data.save('app/static/images/' + filename)
            image = Image(post_id = post.id, name = filename)
            db.session.add(image)
            db.session.commit() 
        return redirect(url_for('index'))
    return render_template("post.html", form=form)

@login_required
@app.route('/post/<int:id>')
def SelectPost(id):
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).where(Post.id == id)
    posts = db.paginate(query, page=page, per_page=1, error_out=False)
    imageQuery = sa.select(Image).where(Image.post_id == id)
    images = db.paginate(imageQuery, page=page, per_page=1, error_out=False)
    commentsQuery = sa.select(Comment).where(Comment.post_id == id).order_by(Comment.timestamp)
    comments = db.paginate(commentsQuery, page=page, per_page=10, error_out=False)
    return render_template("post view.html", posts=posts.items, comments=comments.items, images=images.items)

@login_required
@app.route('/post/<int:parent>/comment', methods=['GET', 'POST'])
def AddComment(parent):
    post = db.session.scalar(sa.select(Post).where(Post.id == parent))
    page = request.args.get('page', 1, type=int)
    imageQuery = sa.select(Image).where(Image.post_id == parent)
    images = db.paginate(imageQuery, page=page, per_page=1, error_out=False)    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comments=form.comment.data, author=current_user, parent=post)
        db.session.add(comment)
        db.session.commit()
        return redirect('/post/' + str(parent))
    return render_template("comment.html", form=form, post=post, images=images.items)

@app.route('/search')
def search():
    searchInput = request.args.get('search')
    Post.reindex()
    results, total = Post.search(searchInput, 1, 5)
    posts = []
    if total != 0:
        posts = results.all()
        results.close()

        for post in posts:
            print(post.title)

    print(posts)

    return render_template("search.html", posts=posts)