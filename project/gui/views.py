
#
# Blueprint for the GUI
#

from flask import Flask, Blueprint, url_for, jsonify, make_response, app, \
        render_template, request, session, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
import requests
import logging
from datetime import datetime
from file_read_backwards import FileReadBackwards

from project.models import *
from project import app, db, is_admin, mail
from project.gui.forms import *
from project.gui.logic import dash_logs, dash_users

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

#
# ROOT PAGE "/"
@gui_blueprint.route("/")
def _index ():

    if current_user.is_authenticated:
        dash = Dashboard.query.all()
        return render_template("dashboard.html", data=dash, logs=dash_logs(), users=dash_users())
    else:
        return redirect(url_for('gui_blueprint._login'))

#
# LOGIN
@gui_blueprint.route("/login", methods=["POST","GET"])
def _login ():

    if request.method=='POST':

        if request.form['login_id'] and request.form['password']:
            user = User.query.filter_by(login_id=request.form['login_id']).first()
            if not user:
                app.logger.warning ("Log in error for " + request.form['login_id'])
                flash('Not account found for ' + request.form['login_id'])
                return render_template("login.html")
            else:
                if user.is_correct_password(request.form['password']):
                    session['login_id'] = request.form['login_id']
                    login_user(user)
                    app.logger.info ("Successfully logged in " + request.form['login_id'])

            if current_user.is_authenticated:
                flash('You were successfully logged in')
                return redirect(url_for('gui_blueprint._index'))
            return render_template("login.html", error="Error with login!")

        else:
            return render_template("login.html", error="Login or password missing!")

    else:
        return render_template("login.html")
#
# LOGOUT
@gui_blueprint.route("/logout", methods=["GET"])
def _logout ():

    if request.method == 'GET':
        if current_user.is_authenticated:
            session['login_id'] = None
            logout_user()
    return redirect(url_for('gui_blueprint._index'))

#
# CHANGES
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

#
# -------------------------------------------------
# ADMIN SECTION
# -------------------------------------------------
@login_required
@gui_blueprint.route("/admin/fortimanagers")
def _fms ():
    if is_admin():
        fms = db.session.query(FortiManager).order_by(FortiManager.id.asc())
        return render_template("fortimanagers.html", data = fms)
    else:
        return render_template("403.html", error = "You are not an administrator")

@login_required
@gui_blueprint.route("/admin/editfm/<id>", methods=["GET","POST"])
def _editfm (id):
    if is_admin():
        fms = db.session.query(FortiManager).order_by(FortiManager.id.asc())
        return render_template("fortimanagers.html", data = fms)
    else:
        return render_template("403.html", error = "You are not an administrator")

@login_required
@gui_blueprint.route("/admin/logs", methods=["GET","POST"])
def _logs ():
    if is_admin():
        counter = request.args.get('counter')
        data = FileReadBackwards(app.config["LOG_FILE"], encoding="utf-8")
        return render_template("logs.html", data = data, counter = counter)
    else:
        return render_template("403.html", error = "You are not an administrator")

@login_required
@gui_blueprint.route("/admin/users", methods=["GET"])
def _users ():
    if is_admin():
        users = db.session.query(User,Role).join(Role).order_by(User.id.asc())
        return render_template("users.html", data = users)
    else:
        return render_template("403.html", error = "You are not an administrator")

@login_required
@gui_blueprint.route("/admin/edituser/<id>", methods=["GET","POST"])
def _edituser (id):
    if is_admin():

        user = User.query.filter_by(id=id).first()
        form = UserForm(obj=user)

        if request.method == "GET":
            return render_template("edituser.html", data = user, form = form)

        if form.validate_on_submit():
            if not user:
                user = User(form.login_id.data, form.forename.data, form.surname.data, form.comment.data, form.password.data, form.email.data, form.role.data)
                db.session.add(user)

            if not form.password.data:
              del form.password

            form.populate_obj(user)
            user.last_modified = datetime.now()
            user.modified_by = session["login_id"]
            user.last_login = datetime.now()

            if not form.created_date:
                user.created_date = datetime.now()

            db.session.commit()
            return redirect(url_for('gui_blueprint._users'))
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print (fieldName + " " + err + " value:(" + form.role.data + ")")
            return render_template("400.html", error = form.errors)

    else:
        return render_template("403.html", error = "You are not an administrator")

@gui_blueprint.route("/search")
def _search ():

    if request.method == 'GET':
        return render_template("search.html")


@gui_blueprint.route("/bookings")
def _bookings ():

    if request.method == 'GET':
        return render_template("calendar.html")

##############
# PARAMETERS #
##############
# Show parameters in a form using a select box to control groupings
@login_required
@gui_blueprint.route("/admin/parameters", methods=["GET","POST"])
def _parameters ():

    if is_admin():
        sel = ParameterSearchForm()
        try:
            print (">" + session["group"] + "<")
        except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)

        if request.method == 'POST':
            sel.param_groups.default = request.form["param_groups"]
            sel.process()
            session["group"] = sel.param_groups.default # save group into session variable for reference.
            params = Parameter.query.filter(Parameter.param_group == sel.param_groups.default).paginate(1, 20, False) # get the currently chosen option from the select list and use to control which parameters are shown
        else:
            try:
                if request.args.get('group'):
                    session["group"] = request.args.get('group')
                    params = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.id == session["group"]).first().id).paginate(1, 20, False) # get the group for the selecter
                else:
                    params = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.param_group == 0).first().id).paginate(1, 20, False) # get the first group for the selecter as we are uisng GET
                    session["group"] = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.param_group == 0).first().id)
            except:
                params = None

        return render_template("parameters.html", data=params, sel=sel, group=session["group"])
    else:
        return render_template("403.html", error = "You are not an administrator")


# Edit Parameter for the application
@login_required
@gui_blueprint.route("/admin/editparameter/<id>", methods=["GET","POST"])
def _editparameter (id):
    if is_admin():

        param = Parameter.query.filter_by(id=id).first()
        grp_form = ParameterSearchForm()
        form = ParameterForm(obj=param)

        if request.method == "GET":
            return render_template("editparameter.html", data=param, grp_form=grp_form, form=form)

        if form.validate_on_submit():
            if not param:
                param = Parameter(form.id.data, form.param_name.data, form.param_value.data, form.param_group.data, form.param_parent.data, form.param_disabled.data)
                db.session.add(param)

            form.populate_obj(param)
            db.session.commit()
            return redirect(url_for('gui_blueprint._parameters'))

        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print (fieldName + " " + err + " value:(" + form.param_name.data + ")")
            return render_template("400.html", error = form.errors)

    else:
        return render_template("403.html", error = "You are not an administrator")






@gui_blueprint.route("/email", methods=["POST","GET"])
def _email ():

    if request.method == "GET":
        if is_admin():
            return render_template("email.html")
        else:
            return render_template("403.html", error = "You are not an administrator")

    if request.method == "POST":
        msg = Message(subject=request.form["subject"],
                      sender=app.config["MAIL_USERNAME"],
                      recipients=request.form["recipient"],
                      body=request.form["body"])
        # mail.send(msg)
        # print (msg.__dict__)
        return render_template("email.html", data = msg)
