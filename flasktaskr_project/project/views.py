# project/views.py


#################
#### imports ####
#################

from project import app, db
from flask import flash, redirect, render_template, session, url_for, request
from functools import wraps
import datetime


###########
# helpers #
###########


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the {0} field - {1}" .format(
                getattr(form, field).label.text, error), 'error')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


##########
# routes #
##########


@app.route('/', defaults={'page': 'index'})
def index(page):
    return redirect(url_for('tasks.tasks'))


@app.errorhandler(404)
def page_not_found(e):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%y %H:%M:%S")
            f.write("'n404 error at {}: {}".format(current_timestamp, r))
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n500 error at {}: {}".format(current_timestamp, r))
    return render_template('500.html'), 500