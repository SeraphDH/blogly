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
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

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

class Tag(db.Model):
    """Add Tags"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100),
                     nullable=False,
                     unique=True)
    posts = db.relationship('Post', secondary = 'posttags',
                            backref = 'tags')

class PostTag(db.Model):
    """Join Posts and Tags"""

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
                        
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)