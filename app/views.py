# views.py

#################
#### imports ####
#################

from flask import Flask, flash, redirect, render_template, request,\
    session, url_for
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
# Add custom form for this app
from forms import AddTaskForm, RegisterForm, LoginForm
import datetime

################
#### config ####
################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Model for this app
from models import Task, User


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You are logged out. Bye. :(')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(
                name=request.form['name'],
                password=request.form['password']).first()
            if u is None:
                error = 'Invalid username or password.'
                return render_template(
                    "login.html",
                    form=form,
                    error=error)
            else:
                session['logged_in'] = True
                session['user_id'] = u.id
                session['role'] = u.role
                flash('You are logged in. Go crazy.')
                return redirect(url_for('tasks'))
        else:
            return render_template(
                "login.html",
                form=form,
                error=error)

    if request.method == 'GET':
        return render_template("login.html", form=form, error=error)

AddTaskForm
# View tasks
@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(Task) \
        .filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task) \
        .filter_by(status='0').order_by(Task.due_date.asc())
    return render_template('tasks.html',
                            form=AddTaskForm(request.form),
                            open_tasks=open_tasks,
                            closed_tasks=closed_tasks)


# Add new tasks
@app.route('/add/', methods=['GET', 'POST'])http://www.apa.org/news/press/releases/2014/03/black-boys-older.aspx
@login_required
def new_task():
    import datetime
    error=None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(form.name.data,
                            form.due_date.data,
                            form.priority.data,
                            datetime.datetime.utcnow(),
                            '1',
                            session['user_id'])
            db.session.add(new_task)
            db.session.commit()
            flash('New entry was successfully posted. Thanks')
            return redirect(url_for('tasks'))
        else:
            return render_template('tasks.html', form=form, error=error)


# Mark tasks as complete:
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.update({"status": "0"})
        db.session.commit()
        flash('The task was marked complete. Nice.')
        return redirect(url_for('tasks'))
    else:
        flash('You can only update tasks that belong to you.')
        return redirect(url_for('tasks'))


# Delete tasks
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.delete()
        db.session.commit()
        flash('The task was deleted. Why not add a new one?')
        return redirect(url_for('tasks'))
    else:
        flash('You can only delete tasks that belong to you.')
        return redirect(url_for('tasks'))


# User Registration:
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'Oh no! That username and/or email already exist. Please try again.'
                return render_template('register.html', form=form, error=error)
        else:
            return render_template('register.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('register.html', form=form)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the {0} field - {1}" .format(
                getattr(form, field).label.text, error), 'error')