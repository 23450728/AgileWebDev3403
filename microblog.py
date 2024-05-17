import sqlalchemy as sa
import sqlalchemy.orm as so
<<<<<<< HEAD
from app import create_app, db
from app.models import User, Post
=======
from app import app, db
from app.models import User, Post, Comment
>>>>>>> e6a729caabe72f9ed618057962c3736424833aa1

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post, 'Comment': Comment}