
#
# Blueprint for the GUI
#

from flask import Flask, Blueprint, url_for, jsonify, make_response, app, \
        render_template, request, session, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
import requests
import logging

from project.models import User, Dashboard, ChangeProfile
from project import app
from project.gui.forms import UserForm, ChangeProfileForm

gui_blueprint = Blueprint('gui_blueprint', __name__, url_prefix="/fpa")

def get_version ():
    session["version"] = app.config["VERSION"]

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

    if current_user.is_authenticated:
        dash = Dashboard.query.all()
        return render_template("dashboard.html", data=dash)
    else:
        return redirect(url_for('gui_blueprint._login'))


# wrapper for the API
@gui_blueprint.route("/login", methods=["POST","GET"])
def _login ():

    if request.method=='POST':

        url = app.config['PROTOCOL'] + app.config['SERVER_NAME'] \
        + "/fpa/api/v1/session"

        if request.form['login_id'] and request.form['password']:

            data = {'login_id':request.form['login_id'], 'password':request.form['password']}
            r = requests.post(url, data)

            login_id = request.form['login_id']
            user = User.query.filter_by(login_id=login_id).first()
            try:
                token = r.json()['token']
                app.logger.info ("Logged in " + login_id + " with token " + token)
                login_user(user)
            except:
                token = None

            session['token'] = token
            session['login_id'] = login_id
            if current_user.is_authenticated:
                flash('You were successfully logged in')
                return redirect(url_for('gui_blueprint._index'))
            return render_template("login.html", error="Error with login!")

        else:
            return render_template("login.html", error="Login or password missing!")

    else:
        return render_template("login.html")

@gui_blueprint.route("/logout", methods=["GET"])
def _logout ():

    if request.method == 'GET':
        if current_user.is_authenticated:
            session['token'] = None
            logout_user()
    return redirect(url_for('gui_blueprint._index'))

@gui_blueprint.route("/admin")
def _admin ():

    if request.method == 'GET':
        if is_loggedin():
            return "ADMIN"
        return "NOT LOGGED IN ADMIN"

@login_required
@gui_blueprint.route("/changes")
def _changes ():

    if request.method == 'GET':
        changes = ChangeProfile.query.order_by(ChangeProfile.id.desc())
        return render_template("changes.html", data = changes)

@login_required
@gui_blueprint.route("/editchange")
def _editchange ():

    if request.method == 'GET':
        changeform = ChangeProfileForm()
        # change = ChangeProfile.query.order_by(ChangeProfile.id.desc())
        return render_template("editchange.html", title='New Change', form = changeform)

@gui_blueprint.route("/search")
def _search ():

    if request.method == 'GET':
        return render_template("search.html")
