from flasketeer import db, login_manager
from flasketeer import bcrypt
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    firstname = db.Column(db.String(length=30), nullable=False)
    lastname = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False, unique=True)
    articles_by = db.relationship("Posts", back_populates="created_by", lazy="dynamic")

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correctness(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Posts(db.Model, UserMixin):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(80), nullable=False)
    post_content = db.Column(db.String, nullable=False)
    # post_image = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    author = db.Column(db.String, nullable=False)
    created_by = db.relationship("Users", back_populates="articles_by")


class Contact(db.Model, UserMixin):
    __tablename__ = 'contact'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    subject = db.Column(db.String(length=80), nullable=False)
    message = db.Column(db.String(), nullable=False, unique=True)
