from flask import render_template, flash, redirect, url_for, request, g, current_app, abort
from app.main.forms import *
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post, Comment
import os
import uuid
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app.main import bp
from app import db
from werkzeug.utils import secure_filename

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_active = datetime.now(timezone.utc)
        db.session.commit()
    g.search_form = SearchForm()

@bp.route('/')
@bp.route('/home/')
def home():   
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).where(Post.file != "").order_by(Post.id.desc())
    posts = db.paginate(query, page=page, per_page=4, error_out=False)
    return render_template("home.html", posts=posts.items)

@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    if current_user.is_authenticated and current_user.email in current_app.config["ADMINS"]:
        return render_template("index.html", posts=posts.items, next_url=next_url, prev_url=prev_url, explore=True, ADMIN=True)
    return render_template("index.html", posts=posts.items, next_url=next_url, prev_url=prev_url, explore=True)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/user/<username>')
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def EditProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template('edit profile.html', form=form)

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        if form.file.data.filename != "":
            filename = secure_filename(form.file.data.filename)
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in [".jpg",".png","jpeg"]:
                abort(400)
            filename = str(uuid.uuid4()) + filename
            form.file.data.save(os.path.join('app/static/images/', filename))
            post = Post(title=form.title.data, body=form.post.data, author=current_user, file = filename)
        else:
            post = Post(title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("post.html", form=form)

@bp.route('/post/<int:id>')
def SelectPost(id):
    page = request.args.get('page', 1, type=int)
    prev = request.args.get('prev', '/index')
    post = db.session.scalar(sa.select(Post).where(Post.id == id))
    commentsQuery = sa.select(Comment).where(Comment.post_id == id).order_by(Comment.timestamp)
    comments = db.paginate(commentsQuery, page=page, per_page=10, error_out=False)
    next_url = url_for('main.SelectPost', id=id, page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.SelectPost', id=id, page=comments.prev_num) \
        if comments.has_prev else None
    return render_template("post view.html", post=post, comments=comments.items, next_url=next_url, prev_url=prev_url, prev=prev)

@bp.route('/post/<int:parent>/comment', methods=['GET', 'POST'])
@login_required
def AddComment(parent):
    post = db.session.scalar(sa.select(Post).where(Post.id == parent))
    prev = prev = request.args.get('prev', '/index')
    page = request.args.get('page', 1, type=int)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comments=form.comment.data, author=current_user, parent=post)
        db.session.add(comment)
        db.session.commit()
        return redirect('/post/' + str(parent))
    return render_template("comment.html", form=form, post=post, prev=prev)

@bp.route('/search')
@login_required
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

    return render_template("search.html", posts=posts, search=True, searchInput=searchInput)