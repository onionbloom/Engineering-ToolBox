import os

import pandas as pd

from bokeh.embed import components
from bokeh.sampledata.iris import flowers as df

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from toolbox import app, bcrypt, db
from toolbox.forms import LaunchEDA, LoginForm, RegistrationForm, UploadForm
from toolbox.plots import stabTrimPlot
from toolbox.models import User


@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', active='active', title='Dashboard')


@app.route('/Flap-Application', methods=['GET', 'POST'])
@login_required
def flapapp():
    # not passing in the data explicitly as Flask-WTF handles passing form data of us
    form = UploadForm()
    eda = LaunchEDA()
    """if form.validate_on_submit() and 'file' in request.files:
        file = request.files.get('file')
        # Convert the FileStorage object from the request into a pandas dataframe
        dataset = pd.read_csv(file)
        dataset['DATETIME'] = pd.to_datetime(dataset['DATETIME'], format="%f" , infer_datetime_format=True)
        plot = stabTrimPlot(dataset)
        script, div = components(plot)
        # secure_filename secures any filename before storing into the system
        filename = secure_filename(file.filename)
        # Save the selected file into the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if file.filename == '':
            flash('No selected file', 'warning')
            return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                                   form=form, eda=eda)

        flash(f'The file {file.filename} was successfully uploaded!', 'success')
        return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                               form=form, eda=eda, filename=filename, script=script, div=div, plotTitle=plot.title.text)"""
    if form.validate_on_submit() and 'file' in request.files:
        file = request.files.get('file')
        # Convert the FileStorage object from the request into a pandas dataframe
        dataset = pd.read_csv(file)
        dataset['DATETIME'] = pd.to_datetime(dataset['DATETIME'], format="%f" , infer_datetime_format=True)
        plot = stabTrimPlot(dataset)
        script, div = components(plot)
        # secure_filename secures any filename before storing into the system
        filename = secure_filename(file.filename)
        # Save the selected file into the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if file.filename == '':
            flash('No selected file', 'warning')
            return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                                   form=form, eda=eda)

        flash(f'The file {file.filename} was successfully uploaded!', 'success')
        return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                               form=form, eda=eda, filename=filename)
        
        if eda.is_submitted():
            flash(f'Your exploratory data analysis is launched')
            return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                               form=form, eda=eda, filename=filename, div=div, script=script, plotTitle=plot.title.text)

    return render_template('flapapp.html', active='active', title='Flap Event Analysis - Create Report', form=form, eda=eda)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate a 12 bit password hash using bcrypt 
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # Assign a new entry into the User db containing the username, email, and hashed password
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You may now login', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Now check if an email is associated to a user AND that the password input equals corresponds to the hash in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Login the user with their option to 'remember-me'
            login_user(user, remember=form.remember.data)
            # Get the next request in a URL that the user wanted to get to, but was prevented because login is required. While args is a dictionary, you could index the key with [], but doing so may give you a key error if it doesn't exist. Hence, the get() method.
            next_page = request.args.get('next')
            # The return is then using a ternary conditional and see if next_page exists
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:    
            flash('Login unsuccessful. Please check email and password. Also make sure that you have registered!', 'danger')

    return render_template('/auth/login.html', title='Login', form=form)

@app.route("/account")
@login_required
def account():
    """ Handles the user's account """
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)

@app.route("/logout")
def logout():
    """ Handles user logout by logging out the user with logout_user function nad redirects the user to the login page """
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
# To handle 404 error, page not found
def page_not_found(error):
    return render_template('404.html'), 404
