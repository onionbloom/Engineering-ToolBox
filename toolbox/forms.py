from wtforms import BooleanField, StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from toolbox.models import User

ALLOWED_EXTENSIONS = ['xls', 'xlsx', 'csv', 'txt']


class RegistrationForm(FlaskForm):
    """ Flask Form to handle user registration """
    username = StringField('Username', validators=[
        DataRequired(), Length(min=5, max=20)])
    email = StringField('User Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up', id='buttonRegister')

    def validate_username(self, username):
        """ This custom validator checks if the input username already exists """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is already taken. Please choose another username.')

    def validate_email(self, email):
        """ This custom validator checks if the input email address already exists """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is already taken. Please choose another username.')


class LoginForm(FlaskForm):
    """ Flask Form to handle user login """
    email = StringField('User Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login', id='buttonSignIn')


class UploadForm(FlaskForm):
    """ Flask Form to handle .csv uploads """
    file = FileField('Upload Raw FDR', validators=[FileRequired(),
                                                   FileAllowed(ALLOWED_EXTENSIONS, 'Only the following extensions are allowed: .xls, .xlsx, .csv, .txt')])
    submit = SubmitField('Select File')


class LaunchEDA(FlaskForm):
    """ Flask Form to launch the exploratory data analysis """
    submit = SubmitField('Launch EDA')
