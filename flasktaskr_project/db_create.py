# db_create.py

from project import db

# create the database and the db table
db.create_all()

# commit the changes
db.session.commit()

'''from project.models import Task, User
from datetime import date

# create the database and the db table
db.create_all()

# insert data
db.session.add(User("admin", "ad@min.com", "admin", "admin"))

db.session.add(Task("Finish this tutorial", date(2015, 11, 14), 10, date(2015, 2, 13), 1, 1))

db.session.add(Task("Finish Real Python", date(2015, 11, 14), 10, date(2015, 2, 13), 1, 1))

# commit the changes
db.session.commit()'''
