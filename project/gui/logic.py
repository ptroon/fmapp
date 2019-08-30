#
# Code for handling queries, database and logic that can be reused.
#

import requests
import logging
from collections import Counter

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

    print (res)
    return res
