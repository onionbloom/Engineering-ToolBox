from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegistrationForm(Form):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('User Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up', id='buttonRegister')


class LoginForm(Form):
    email = StringField('User Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login', id='buttonSignIn')

class FileSelect(Form):
    file = FileField('Browse File', validators=[DataRequired(), Regexp('([^\\s]+(\\.(?i)(xls?x|csv|txt|mhtml))$)')])
    submit = SubmitField('Select File', id='buttonRegister')