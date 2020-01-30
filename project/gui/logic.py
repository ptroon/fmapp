#
# Code for handling queries, database and logic that can be reused.
#

import requests
import logging
from collections import Counter
from flask import flash
from datetime import datetime

from project.models import User, Role, Dashboard, ChangeProfile
from project import app, db, is_admin

# Works out how many types of messages the log has
# returns a dict with each type and a count
def dash_logs ():
    _file = open(app.config["LOG_FILE"], 'r')
    patterns = ["INFO", "DEBUG", "WARNING", "CRITICAL"]
    results = {pattern:Counter() for pattern in patterns}
    for line in _file:
       for pattern in patterns:
           if pattern in line:
               results[pattern][line] += 1

    res = {}
    for x in results:
        res[x] = len(results[x])

    # print (res)
    return res

# Returns all users for dashboard
def dash_users ():
    user = User.query.filter_by().all()

    res = {}
    for x in user:
        res[x] = len(user)

    return user


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'warning')


# takes a week_string in the format of e.g. 'NYNNYNN'
# plus a date_string in the format of e.g. '20-01-2020'
# It determines the day of the week from the date_string
# then works out if the date_string is one of the 'Y' or 'N' in the
# week_string
def is_day_allowed(date_string, week_string):
    try:
        # create a datetime object from the string and check weekday to get a number 0-6
        day_of_week = datetime.strptime(date_string, '%d-%m-%Y').weekday()
        # we should have the DoW as e.g. Mon=0
        if week_string[day_of_week] == 'Y':
            return True
        else:
            return False

    except:
        return False # failed to convert string or not valid so return false


def json_fmt_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isInstance(o, InstanceState):
        pass
