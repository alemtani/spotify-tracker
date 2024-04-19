from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import HiddenField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional, ValidationError

from . import bcrypt
from .models import User

""" *** User forms *** """

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')
    
    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    about = TextAreaField('About', validators=[Optional()])
    submit_account = SubmitField('Update Account')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None and user != current_user:
            raise ValidationError('Username is taken')

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images Only')
    ])
    submit_picture = SubmitField('Update Profile Picture')

class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        InputRequired(), 
        EqualTo('new_password', 'Passwords must match')
    ])
    submit_password = SubmitField('Update Password')

    def validate_old_password(self, old_password):
        password_match = bcrypt.check_password_hash(current_user.password, old_password.data)
        if not password_match:
            raise ValidationError('Old password is incorrect')

""" *** Player forms *** """

class AddPlayerForm(FlaskForm):
    submit_add = SubmitField('Add')

class DeletePlayerForm(FlaskForm):
    submit_delete = SubmitField('Delete')

class EditAlbumPlayerForm(FlaskForm):
    total_tracks = IntegerField(widget=HiddenField())
    listened_tracks = IntegerField('Listened Tracks', validators=[InputRequired()])
    status = SelectField('Status', choices=[
        ('added', 'Added'), 
        ('listening', 'Listening'), 
        ('done', 'Done')
    ], validators=[InputRequired()])
    submit = SubmitField('Submit')

    def validate_listened_tracks(self, listened_tracks):
        if listened_tracks.data < 0:
            raise ValidationError('Listened tracks cannot be negative')
        if listened_tracks.data > self.total_tracks.data:
            raise ValidationError('Listened tracks cannot exceed total tracks')

class EditTrackPlayerForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('added', 'Added'), 
        ('listening', 'Listening'), 
        ('done', 'Done')
    ], validators=[InputRequired()])
    submit = SubmitField('Submit')

