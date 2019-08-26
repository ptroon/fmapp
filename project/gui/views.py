
#
# Blueprint for the GUI
#

from flask import Flask, Blueprint, url_for, jsonify, make_response, app, \
        render_template, request, session, redirect
from flask_login import login_required, login_user, logout_user, current_user
import requests

from project.models import User
from project import app

gui_blueprint = Blueprint('gui_blueprint', __name__, url_prefix="/fpa")

# Checks to see if token is set as a session variable
def is_loggedin ():
    try:
        if session['token']:
            return True
        else:
            return False
    except:
        return False


@gui_blueprint.route("/")
def _index ():

    if is_loggedin() or current_user.is_authenticated:
        return render_template("base.html")
    else:
        return render_template("login.html")


# wrapper for the API
@gui_blueprint.route("/login", methods=["POST","GET"])
def _login ():

    url = app.config['PROTOCOL'] + app.config['SERVER_NAME'] \
        + "/fpa/api/v1/session"

    if request.form['login_id'] and request.form['password']:

        data = {'login_id':request.form['login_id'], 'password':request.form['password']}
        r = requests.post(url, data)

        user = User.query.filter_by(login_id=request.form['login_id']).first()
        try:
            token = r.json()['token']
            print (r.text)
            login_user(user)
        except:
            token = None

        session['token'] = token
        if is_loggedin() or current_user.is_authenticated:
            return redirect(url_for('gui_blueprint._index'))
        return render_template("login.html", error="Error with login!")

    else:
        return render_template("login.html", error="Login or password missing!")

@gui_blueprint.route("/logout", methods=["GET"])
def _logout ():

    if request.method == 'GET':
        if is_loggedin() or current_user.is_authenticated:
            session['token'] = None
            logout_user()
    return redirect(url_for('gui_blueprint._index'))

@gui_blueprint.route("/admin")
def _admin ():

    if request.method == 'GET':
        if is_loggedin():
            return "ADMIN"
        return "NOT LOGGED IN ADMIN"


@gui_blueprint.route("/changes")
def _changes ():

    if request.method == 'GET':
        return "CHANGES"


@gui_blueprint.route("/register")
def _register ():

    if request.method == 'GET':
        return "REGISTER"
