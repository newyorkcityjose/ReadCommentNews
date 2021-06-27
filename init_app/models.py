from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class User(db.Model, UserMixin):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key=True )
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    bio = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.String(64), default="avatar1.png")
    
    @classmethod
    def signup(cls, *args, **kwargs):
        """sign up and hashes password """
        password = kwargs.get("password")
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        kwargs["password"] = hashed_pwd
        user = User(**kwargs)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """
        Find username and password         
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @property
    def get_profile_image(self):
        return url_for('static', filename='image/user_profile/' + self.profile_image)


class Bookmark(db.Model):
    """Mapping user likes to profile"""

    __tablename__= 'bookmark'

    id = db.Column(db.Integer, primary_key=True)
    bookmark = db.Column(db.Text)
    news = db.Column(db.Text)
    description = db.Column(db.Text) 
    url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    author = db.relationship(User, foreign_keys=user_id, backref='author', lazy=True)

class Comment(db.Model):
    """Comments for users"""
    __tablename__ = "comment"

    id= db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    bookmark = db.Column(db.Integer, db.ForeignKey('bookmark.id', ondelete='cascade'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    parent_comment = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='cascade'))
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    comment_author = db.relationship(User, foreign_keys=user_id, backref='comment_author', lazy=True)
    parent_comment_rel = db.relationship(lambda: Comment, remote_side=id, backref='comment_parents', lazy=True)

class Follower(db.Model):
    """Follwers for user table"""
    __tablename__ = "follower"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user_follower_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    follows = db.relationship(User, foreign_keys=user_id, backref='follows', lazy=True)
    followers = db.relationship(User, foreign_keys=user_follower_id, backref='followers', lazy=True)

inbox_discussion_rel = db.Table(
    'inbox_discussion_rel', db.Model.metadata,
    db.Column('discussion_id', db.Integer, db.ForeignKey('discussion.id')),
    db.Column('inbox_id', db.Integer, db.ForeignKey('inbox.id'))
)

class Discussion(db.Model):
    """Discussion model"""
    __tablename__ = 'discussion'

    id = db.Column(db.Integer, primary_key=True)
    user_dis_start_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user_dis_follow_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    title = db.Column(db.Text)
    inbox_messages = db.relationship('Inbox', secondary=inbox_discussion_rel)

    user_dis_start = db.relationship(User, foreign_keys=user_dis_start_id, backref='user_dis_start', lazy=True)
    user_dis_follow = db.relationship(User, foreign_keys=user_dis_follow_id, backref='user_dis_follow', lazy=True)

class Inbox(db.Model):
    """Inbox for user messages"""
    __tablename__ = 'inbox'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    title = db.Column(db.Text)
    message = db.Column(db.Text)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author_message = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    user = db.relationship(User, foreign_keys=user_id, backref='user', lazy=True)
    message_from = db.relationship(User, foreign_keys=author_message, backref='message_from', lazy=True)



    

