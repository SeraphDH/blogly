from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()


class user(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(25),
                           nullable=False,
                           unique=False)
    last_name = db.Column(db.String(25),
                           nullable=False,
                           unique=False)
    image_url = db.Column(db.String(200),
                          nullable=True)
    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    """Blog Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=db.func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
