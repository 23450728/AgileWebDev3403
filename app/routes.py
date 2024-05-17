from flask import render_template, flash, redirect, url_for, request, g
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import *
from urllib.parse import urlsplit

@app.before_request
def before_request():
    g.search_form = SearchForm()

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", posts=posts.items, next_url=next_url, prev_url=prev_url, explore=True)


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

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def EditProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template('edit profile.html', form=form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("post.html", form=form)

@login_required
@app.route('/post/<int:id>')
def SelectPost(id):
    page = request.args.get('page', 1, type=int)
    prev = request.args.get('prev', '/index')
    post = db.session.scalar(sa.select(Post).where(Post.id == id))
    commentsQuery = sa.select(Comment).where(Comment.post_id == id).order_by(Comment.timestamp)
    comments = db.paginate(commentsQuery, page=page, per_page=10, error_out=False)
    next_url = url_for('SelectPost', id=id, page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('SelectPost', id=id, page=comments.prev_num) \
        if comments.has_prev else None
    return render_template("post view.html", post=post, comments=comments.items, next_url=next_url, prev_url=prev_url, prev=prev)

@login_required
@app.route('/post/<int:parent>/comment', methods=['GET', 'POST'])
def AddComment(parent):
    post = db.session.scalar(sa.select(Post).where(Post.id == parent))
    prev = prev = request.args.get('prev', '/index')
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comments=form.comment.data, author=current_user, parent=post)
        db.session.add(comment)
        db.session.commit()
        return redirect('/post/' + str(parent))
    return render_template("comment.html", form=form, post=post, prev=prev)

@login_required
@app.route('/post/<int:id>/like', methods=['GET', 'POST'])
def LikePost(id):
    post = db.session.scalar(sa.select(Post).where(Post.id == id))

    if current_user.is_anonymous:
        return redirect('/login?next=/post/' + str(id))

    if current_user in post.liked_by:
        statement = user_likes.delete().where(user_likes.c.post_id == post.id, user_likes.c.user_id == current_user.id)
    else:
        statement = user_likes.insert().values(post_id=post.id, user_id=current_user.id)

    db.session.execute(statement)
    db.session.commit()
    return redirect('/post/' + str(id))

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

    return render_template("search.html", posts=posts, search=True, searchInput=searchInput)