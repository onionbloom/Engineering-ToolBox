from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (BooleanField, PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from toolbox.models import User

ALLOWED_EXTENSIONS = ['xls', 'xlsx', 'csv', 'txt']


class RegistrationForm(FlaskForm):
    """ Flask Form to handle user registration """
    username = StringField('Username', validators=[
        DataRequired(), Length(min=5, max=20)], render_kw={"autocomplete": "off"})
    email = StringField('User Email', validators=[DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up', id='buttonRegister')

    def validate_username(self, username):
        """ This custom in-line validator checks if the input username already exists """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is already taken. Please choose another username.')

    def validate_email(self, email):
        """ This custom in-line validator checks if the input email address already exists """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is already taken. Please choose another username.')


class LoginForm(FlaskForm):
    """ Flask Form to handle user login """
    email = StringField('User Email', validators=[
                        DataRequired(), Email()], render_kw={"autocomplete": "off"})
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Continue', id='buttonSignIn')


class UploadForm(FlaskForm):
    """ Flask Form to handle .csv uploads """
    file = FileField('Select File', validators=[FileRequired(),
                                                   FileAllowed(ALLOWED_EXTENSIONS, 'Only the following extensions are allowed: .xls, .xlsx, .csv, .txt')])
    submit = SubmitField('Upload File')

class EDAForm(FlaskForm):
    """ Flask Form to handle selecting the available clean dfdr .csv to perform the chosen analysis """
    dfdr = SelectField('Choose Dataframe')
    registration = SelectField('Registration', id='registration')
    flight_no = SelectField('Flight Number', id='flight_no')
    date = SelectField('Date', id='date')
    # No choices arguements are defined in this declaration as we will define them dynamically in the view functions in routes.py 
    submit = SubmitField('Launch EDA', _name='launchEDA')

"""
class EDAForm(FlaskForm):
    file = FileField('Select File', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Only the following extensions are allowed: .xls, .xlsx, .csv, .txt')])
    submit = SubmitField('Upload File')"""