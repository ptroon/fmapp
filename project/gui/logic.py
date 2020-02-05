#####################################################################
# Code for handling queries, database and logic that can be reused. #
#####################################################################

import requests
import logging
from collections import Counter
from flask import flash
from datetime import datetime, timedelta

from project.models import *
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

    return res


# Flashes the errors contained in the form
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



# Checks a complex start & end push times
# compares to the provided start and end times
# if the booking has different times then return True
# if not different return False
# True means approval needed as custom times used.
def is_booking_custom(start_t, end_t, complex_id):

    q1 = Complex.query.filter(Complex.id==int(complex_id)).first()
    if q1.complex_push_start == start_t and q1.complex_push_end == end_t:
        return False # this is the same timing
    else:
        return True # approval needed as this is different



# takes input of date string e.g. '01/01/2020' and complex id
# q1 - checks this change not over total changes p/day
# q2 - checks this change not over total for complex p/day
# q3 - checks this change not over total for diff complexes p/day
def is_booking_core_ok(date_str, complex_id):

    date_s = datetime.strptime(date_str, '%d/%m/%Y') # start date with 00:00:00
    date_e = date_s + timedelta(minutes=1439) # end date with 23:59:00

    # get a count of all bookings where booking start between date_s and date_e
    q1 = db.session.query(Booking.id).filter(Booking.start_dt.between(date_s, date_e)).count()

    #q2 = db.session.query(Booking.id).filter(Booking.complex==complex_id).filter(Booking.start_dt)
    return True


'''
def json_fmt_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isInstance(o, InstanceState):
        pass
'''
