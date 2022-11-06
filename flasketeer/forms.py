from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flasketeer.models import Users, Posts
import re


class RegisterForm(FlaskForm):
    def validate_username(self, user_name_to_check):
        user = Users.query.filter_by(username=user_name_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
        elif re.findall('\W', user_name_to_check.data):
            raise ValidationError('Username must have only characters from a-Z, digits from 0-9, and underscore (_)')

    def validate_email_address(self, email_address_to_check):
        email_address = Users.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    def validate_firstname(self, first_name_to_check):
        if re.findall('\W', first_name_to_check.data):
            raise ValidationError('Firstname must have only characters from a-Z, digits from 0-9, and underscore (_)')

    def validate_lastname(self, last_name_to_check):
        if re.findall('\W', last_name_to_check.data):
            raise ValidationError('Lastname must have only characters from a-Z, digits from 0-9, and underscore (_)')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    firstname = StringField(label='Firstname:', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(label='Lastname:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    confpassword = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign in')


class PostForm(FlaskForm):
    def validate_post_title(self, title_to_check):
        post_title_exist = Posts.query.filter_by(post_title=title_to_check.data).first()
        if post_title_exist:
            raise ValidationError('Post title has already been used! Please try to be more specific')

    def validate_post_content(self, content_to_check):
        post_content_exist = Posts.query.filter_by(post_title=content_to_check.data).first()
        if post_content_exist:
            raise ValidationError('Post content has already been used! Please avoid plagiarism')

    post_title = StringField(label='Title', validators=[Length(min=2, max=80), DataRequired()])
    post_content = TextAreaField(label='Body', validators=[Length(min=50), DataRequired()])
    submit = SubmitField(label='Post')

class EditForm(FlaskForm):
    def validate_post_title(self, title_to_check):
        post_title_exist = Posts.query.filter_by(post_title=title_to_check.data).first()
        if post_title_exist:
            raise ValidationError('Post title has already been used! Please try to be more specific')

    def validate_post_content(self, content_to_check):
        post_content_exist = Posts.query.filter_by(post_title=content_to_check.data).first()
        if post_content_exist:
            raise ValidationError('Post content has already been used! Please avoid plagiarism')

    post_title = StringField(label='Title', validators=[Length(min=2, max=80), DataRequired()])
    post_content = TextAreaField(label='Body', validators=[Length(min=50, max=1024), DataRequired()])
    submit = SubmitField(label='Post')


class ContactForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    subject = StringField(label='Subject:', validators=[Length(min=2, max=80), DataRequired()])
    message = TextAreaField(label='Message:', validators=[Length(min=2), DataRequired()])
    submit = SubmitField(label='Submit')