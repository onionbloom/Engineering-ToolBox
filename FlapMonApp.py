import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, Renderer
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.sampledata.iris import flowers as df  # Temporary sample dataset
from plots import petal_sepal_scatter

from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
from forms import RegistrationForm, LoginForm, FileSelect


# Specify the application's root so Python may know where to look for templates, and static files.
app = Flask(__name__)

app.config['SECRET_KEY'] = 'R3YU9hssXvaBWT9R'


@app.route('/', methods=['GET', 'POST'])
# Routing to the index page (when signed in)
def dashboard():
    form = FileSelect(request.form)
    plot = petal_sepal_scatter(df)
    script, div = components(plot)
    if request.method == 'POST' and form.validate():
        flash(f'The file you selected was: {form.file.data}!', 'success')
    return render_template('dashboard.html', active='active', title='Dashboard', form=form, script=script, div=div, plotTitle=plot.title.text)


@app.route('/Flap-Application', methods=['GET', 'POST'])
def flapapp():

    return render_template('flapapp.html', active='active', title='Flap Event Analysis')


@app.route('/register', methods=['GET', 'POST'])
# The register page
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
# The login page
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Welcome back, brave engineer! This is your dashboard.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Unsuccessful login. If you already have an account, please verify correct email and password.', 'danger')

    return render_template('/auth/login.html', title='Login', form=form)


@app.errorhandler(404)
# To handle 404 error, page not found
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # This will only ever be true when you run the app with Python directly
    app.run(debug=True)  # Run in debug mode
