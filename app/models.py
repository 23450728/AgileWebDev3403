from datetime import datetime, timezone
from typing import Optional, List, Set
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login, search
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = search.query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return [], 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        query = sa.select(cls).where(cls.id.in_(ids)).order_by(
            db.case(*when, value=cls.id))
        return db.session.scalars(query), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                search.add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                search.add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                search.remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in db.session.scalars(sa.select(cls)):
            search.add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    bio: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_active: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='author')
    liked_posts: so.Mapped[Set['Post']] = so.relationship('Post', secondary='user_likes', back_populates='liked_by')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        hex = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{hex}?d=identicon&s={size}'
    
    def posts_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.posts.select().subquery())
        return db.session.scalar(query)

class Post(SearchableMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc)) 
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    comments: so.Mapped[List['Comment']] = so.relationship(back_populates='parent')
    liked_by: so.Mapped[Set['User']] = so.relationship('User', secondary='user_likes', back_populates='liked_posts')

    __searchable__ = ['title', 'body', 'author.username']

    def __repr__(self):
        return '<Post {}>'.format(self.body)
 
    def comments_count(self):
        return len(self.comments) if self.comments != None else 0
    
    def likes_count(self):
        return len(self.liked_by) if self.liked_by != None else 0

user_likes = db.Table('user_likes',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    comments: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='comments')
    parent: so.Mapped[Post] = so.relationship(back_populates='comments')


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))