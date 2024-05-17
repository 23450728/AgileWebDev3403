from config import Config
from datetime import datetime, timezone, timedelta
import unittest
import sqlalchemy as sa
from config import TestConfig
from app import create_app, db
from app.models import User, Post, Comment


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
    
    def test_post_count(self):
        u = User(username='susan', email='susan@example.com')
        db.session.add(u)
        now = datetime.now(timezone.utc)
        p1 = Post(title="title", body="post from susan", author=u,
                  timestamp=now + timedelta(seconds=1))
        db.session.add(p1)
        self.assertFalse(u.posts_count() == 2)
        self.assertTrue(u.posts_count() == 1)

    def test_post_comment(self):
        u = User(username='susan', email='susan@example.com')
        db.session.add(u)
        now = datetime.now(timezone.utc)
        p1 = Post(title="title", body="post from susan", author=u,
                  timestamp=now + timedelta(seconds=1))        
        db.session.add(p1)
        c1 = Comment(comments="Comment", author=u, parent=p1)
        db.session.add(c1)
        self.assertTrue(p1.comments_count() == 1)
        self.assertFalse(p1.comments_count() == 2)

    def test_duplicate_usernames(self):
        u1 = User(username='susan', email='susan1@example.com')
        db.session.add(u1)
        try:
            u2 = User(username='susan', email='susan2@example.com')
            db.session.add(u2)
        except:
            user = db.session.scalar(sa.select(User).where(User.username == 'susan'))
            self.assertTrue(user == 1)
    
    def test_duplicate_emails(self):
        u1 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        try:
            u2 = User(username='susan1', email='susan@example.com')
            db.session.add(u2)
        except:
            user = db.session.scalar(sa.select(User).where(User.email == 'susan@example.com'))
            self.assertTrue(user == 1)
    
    def test_images(self):
        u1 = User(username='susan', email='susan@example.com')
        db.session.add(u1)

        now = datetime.now(timezone.utc)
        p1 = Post(title="title", body="post from susan", author=u1,
                  timestamp=now + timedelta(seconds=1))        
        db.session.add(p1)

        now = datetime.now(timezone.utc)
        p2 = Post(title="title", body="post from susan", file="test.png", author=u1, timestamp=now + timedelta(seconds=1))        
        db.session.add(p2)
        
        post = db.session.scalar(sa.select(Post).where(Post.file != ''))
        self.assertTrue(post == 1)
