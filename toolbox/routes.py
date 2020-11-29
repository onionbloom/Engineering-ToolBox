import os

import pandas as pd

from bokeh.embed import components
from bokeh.sampledata.iris import flowers as df

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from toolbox import app, bcrypt, db
from toolbox.forms import LoginForm, RegistrationForm, UploadForm, EDAForm
from toolbox.plots import stabTrimPlot, flapAsymPlot
from toolbox.models import User, Clean_dfdr
from toolbox.dfdr_parser import DfdrConverter
from toolbox.flap_monitoring import FlapDataExtractor

from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        day = datetime.now().strftime("%A")
        date = datetime.now().strftime("%d")
        month = datetime.now().strftime("%B")
        year = datetime.now().strftime("%Y")
        time = datetime.now().strftime("%H:%M")
        return render_template('dashboard.html', active='active', title='Dashboard', username=current_user.username, day=day, date=date, month=month, year=year, time=time)

    return redirect(url_for('login'))


@app.route('/Flap-Application', methods=['GET', 'POST'])
@login_required
def flapapp():
    # not passing in the data explicitly as Flask-WTF handles passing form data for us
    form = UploadForm()
    form_EDA = EDAForm()
    form_EDA.registration.choices = [g.ac_reg for g in Clean_dfdr.query.order_by('ac_reg').all()]
    form_EDA.flight_no.choices = [g.flight_no for g in Clean_dfdr.query.order_by('flight_no').all()]
    form_EDA.date.choices = [g.datetime for g in Clean_dfdr.query.order_by('datetime').all()]
    day = datetime.now().strftime("%A")
    date = datetime.now().strftime("%d")
    month = datetime.now().strftime("%B")
    year = datetime.now().strftime("%Y")
    time = datetime.now().strftime("%H:%M")

    return render_template('flapapp.html', active='active', title='Flap Event Analysis - Create Report', form=form, form_EDA=form_EDA, username=current_user.username, day=day, date=date, month=month, year=year, time=time)


@app.route('/raw', methods=['POST'])
def raw():
    form = UploadForm()
    form_EDA = EDAForm()
    form_EDA.registration.choices = [ (g.ac_reg) for g in Clean_dfdr.query.order_by('ac_reg').all()]
    form_EDA.flight_no.choices = [g.flight_no for g in Clean_dfdr.query.order_by('flight_no').all()]
    form_EDA.date.choices = [g.datetime for g in Clean_dfdr.query.order_by('datetime').all()]
    if form.validate_on_submit() and 'file' in request.files:
        day = datetime.now().strftime("%A")
        date = datetime.now().strftime("%d")
        month = datetime.now().strftime("%B")
        year = datetime.now().strftime("%Y")
        time = datetime.now().strftime("%H:%M")
        file = request.files.get('file')
        # secure_filename secures any filename before storing into the system
        filename = secure_filename(file.filename)
        # Convert the FileStorage object from the request into a pandas dataframe and parse through the data to
        # get a clean and pandas friendly .csv, then upload it.
        dfdr_df = DfdrConverter(file=file, output_path=app.config['UPLOAD_FOLDER'], filename=filename, separator=';')
        ac_reg = dfdr_df.obtain_ac_reg()
        df_type = dfdr_df.dataframe_selection(ac_reg)
        dfdr_df.dfdr_tidy(dataframe_type=df_type)
        print(dfdr_df.date)
        clean_dfdr = Clean_dfdr(ac_reg=dfdr_df.ac_reg, flight_no=dfdr_df.flight_no, datetime=dfdr_df.date)
        db.session.add(clean_dfdr)
        db.session.commit()
        Clean_dfdr.query.all()
        if file.filename == '':
            flash('No selected file', 'warning')
            return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                                   form=form, form_EDA=form_EDA, username=current_user.username, day=day, date=date, month=month, year=year, time=time)

        flash(
            f'The file {file.filename} was successfully uploaded!', 'success')
        return redirect(url_for('flapapp'))

    return redirect(url_for('flapapp'))


@app.route('/launchEDA', methods=['POST'])
def launchEDA():
    form = UploadForm()
    form_EDA = EDAForm()
    form_EDA.registration.choices = [ (g.ac_reg) for g in Clean_dfdr.query.order_by('ac_reg').all()]
    form_EDA.flight_no.choices = [g.flight_no for g in Clean_dfdr.query.order_by('flight_no').all()]
    form_EDA.date.choices = [g.datetime for g in Clean_dfdr.query.order_by('datetime').all()]
    if form_EDA.validate_on_submit():
        day = datetime.now().strftime("%A")
        date = datetime.now().strftime("%d")
        month = datetime.now().strftime("%B")
        year = datetime.now().strftime("%Y")
        time = datetime.now().strftime("%H:%M")
        # Convert the FileStorage object from the request into a pandas dataframe and parse through the data to
        # get a clean and pandas friendly .csv, then upload it.
        if form_EDA.EDA_type.data == 'Asym':
            plot, plot2 = flapAsymPlot(registration=form_EDA.registration.data, flight_no=form_EDA.flight_no.data, date=form_EDA.date.data, output_folder=app.config['UPLOAD_FOLDER'])
            plotTitle = plot.title.text
            plotTitle2 = plot2.title.text
            script, div = components(plot)
            script2, div2 = components(plot2)
            flash(f'Below is your exploratory Flap Asymmetry analysis!', 'success')
            return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                                div=div, script=script, plotTitle=plotTitle, div2=div2, script2=script2, plotTitle2=plotTitle2,
                                form=form, form_EDA=form_EDA, username=current_user.username, day=day, date=date, month=month, year=year, time=time)
        else:
            plot, plot2 = stabTrimPlot(registration=form_EDA.registration.data, flight_no=form_EDA.flight_no.data, date=form_EDA.date.data, output_folder=app.config['UPLOAD_FOLDER'])
            plotTitle = plot.title.text
            plotTitle2 = plot2.title.text
            script, div = components(plot)
            script2, div2 = components(plot2)

            flash(f'Below is your exploratory Stabilizer Trim Event analysis!', 'success')
            return render_template('flapapp.html', active='active', edaLaunchable='true', title='Flap Event Analysis - Create Report',
                                div=div, script=script, plotTitle=plotTitle,  div2=div2, script2=script2, plotTitle2=plotTitle2,
                                form=form, form_EDA=form_EDA, username=current_user.username, day=day, date=date, month=month, year=year, time=time)

    return redirect(url_for('flapapp'))


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
        flash(
            f'Account created for {form.username.data}! You may now login', 'success')
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
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
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
