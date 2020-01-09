
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
from project import app, db, is_admin, mail, get_user
from project.gui.forms import *
from project.gui.logic import *

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

#################################################################
# ROOT #
########
@gui_blueprint.route("/")
def _index ():

    if current_user.is_authenticated:
        dash = Dashboard.query.all()
        return render_template("dashboard.html", data=dash, logs=dash_logs(), users=dash_users())
    else:
        return redirect(url_for('gui_blueprint._login'))

#################################################################
# LOGIN #
#########
@gui_blueprint.route("/login", methods=["POST","GET"])
def _login ():

    form = UserForm()
    if request.method=='POST':

        if request.form['login_id'] and request.form['password']:
            user = User.query.filter_by(login_id=request.form['login_id']).first()
            if not user:
                app.logger.warning ("Log in error for " + request.form['login_id'] + ", no account found")
                flash('No account found for ' + request.form['login_id'], 'warning')
                return render_template("login.html", form=form)
            else:
                if user.is_correct_password(request.form['password']):
                    session['login_id'] = request.form['login_id']
                    login_user(user)
                    app.logger.info ("Successfully logged in " + request.form['login_id'])

            if current_user.is_authenticated:
                flash('You were successfully logged in', 'success')
                return redirect(url_for('gui_blueprint._index'))

            flash('Error with login!', 'warning')
            return render_template("login.html", form=form)

        else:
            flash('Login or password missing!', 'warning')
            return render_template("login.html", form=form)

    else:
        return render_template("login.html", form=form)

#################################################################
# LOGOUT #
##########
@gui_blueprint.route("/logout", methods=["GET"])
def _logout ():

    if request.method == 'GET':
        if current_user.is_authenticated:
            session['login_id'] = None
            logout_user()
    return redirect(url_for('gui_blueprint._index'))

#################################################################
# REGISTER #
############
@gui_blueprint.route("/register", methods=["GET", "POST"])
def _register ():

    form = UserForm()
    form.savebtn.label.text = 'Register'
    if request.method == 'GET':
        return render_template("register.html", form=form)

    if form.validate_on_submit():
        return render_template("register.html", form=form)
    else:
        flash_errors(form)
        return render_template("register.html", form=form)

#################################################################
# CHANGES #
###########
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


#################################################################
# FORTIMANAGERS #
#################
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

#################################################################
# LOGS #
########
@login_required
@gui_blueprint.route("/admin/logs", methods=["GET","POST"])
def _logs ():
    if is_admin():

        form = LogForm()

        # Prevent the rec # counter from breaking the app - default to 10
        try:
            records = int(request.args.get('log_records'))
        except:
            records = 5

        # Prevent the log name from breaking the app - default to LOG_FILE variable
        try:
            rec_t = request.args.get('log_options')
            log_t   = app.config[rec_t]
        except:
            log_t = app.config["LOG_FILE"]

        form.log_records.data = str(records)
        form.log_options.data = rec_t
        data = FileReadBackwards(log_t, encoding="utf-8")
        return render_template("logs.html", data=data, form=form, counter=records)
    else:
        return render_template("403.html", error = "You are not an administrator")

#################################################################
# USERS #
#########
@login_required
@gui_blueprint.route("/admin/users", methods=["GET"])
def _users ():
    if is_admin():
        users = db.session.query(User,Role,Parameter).join(Role).outerjoin(Parameter).order_by(User.id.asc())
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

#################################################################
# ROLES #
#########
@login_required
@gui_blueprint.route("/admin/roles", methods=["GET"])
def _roles ():
    if is_admin():
        roles = Role.query.order_by(Role.id.asc())
        return render_template("roles.html", data = roles)
    else:
        return render_template("403.html", error = "You are not an administrator")


@login_required
@gui_blueprint.route("/admin/editrole/<id>", methods=["GET","POST"])
def _editrole (id):

    if is_admin():

        role = Role.query.filter_by(id=id).first()
        form = RoleForm(obj=role)

        if request.method == "GET":
            return render_template("editrole.html", form=form, data=role)

        if form.validate_on_submit():

            if form.savebtn.data:
                if not role:
                    role = Role(form.role_name.data, form.role_admin.data, form.role_app_sections.data, form.enabled.data)
                    db.session.add(role)

                form.populate_obj(role)
                db.session.commit()
                flash ('Role saved successfully', 'success')
                return redirect(url_for('gui_blueprint._roles'))

            if form.deletebtn.data:
                role = Role.query.filter_by(id=id).first()
                counter = User.query.filter_by(role=role.id).count()
                if counter == 0:  # there are no user accounts using this role
                    db.session.delete(role)
                    flash ('Role removed successfully', 'success')
                    db.session.commit()
                else:
                    flash ('Cannot delete role as it is in use', 'warning')

                return redirect(url_for('gui_blueprint._roles'))

#################################################################
# DATES #
#########
@login_required
@gui_blueprint.route("/admin/dates", methods=["GET"])
def _dates ():
    if is_admin():
        dates = DateOfInterest.query.order_by(DateOfInterest.id.asc())
        return render_template("dates.html", data=dates)
    else:
        return render_template("403.html", error = "You are not an administrator")

@login_required
@gui_blueprint.route("/admin/editdate/<id>", methods=["GET","POST"])
def _editdate (id):

    if is_admin():

        doi = DateOfInterest.query.filter_by(id=id).first()
        form = DOIForm(obj=doi)

        if request.method == "GET":
            return render_template("editdate.html", form=form, data=doi)

        if form.validate_on_submit():

            if form.savebtn.data:
                if not doi:
                    doi = DateOfInterest(form.doi_name.data, form.doi_priority.data, form.doi_comment.data, form.doi_start_dt.data, form.doi_end_dt.data)
                    db.session.add(doi)

                form.populate_obj(doi)
                db.session.commit()
                flash ('Date saved successfully', 'success')
                return redirect(url_for('gui_blueprint._dates'))

            if form.deletebtn.data:
                doi = DateOfInterest.query.filter_by(id=id).first()
                db.session.delete(doi)
                flash ('Date removed successfully', 'success')
                db.session.commit()

        else:
            flash_errors(form)

        return redirect(url_for('gui_blueprint._dates'))


    else:
        return render_template("403.html", error = "You are not an administrator")

#################################################################
#  #
#########
@gui_blueprint.route("/search", methods=["POST"])
def _search ():

    form = MainSearchForm()
    results = db.session.query(Parameter.param_name.label("result")).filter(Parameter.param_group>0).order_by(Parameter.param_name.asc())
    if request.method == 'POST':
        return render_template("search.html", query=request.form.getlist('query')[0], results=results, form=form)


@gui_blueprint.route("/bookings")
def _bookings ():

    if request.method == 'GET':
        return render_template("calendar.html")


#################################################################
# PARAMETERS #
##############
# Show parameters in a form using a select box to control groupings
@login_required
@gui_blueprint.route("/admin/parameters", methods=["GET","POST"])
def _parameters ():

    if is_admin():
        sel = ParameterSearchForm()

        if request.method == 'POST':
            sel.param_groups.default = request.form["param_groups"]
            sel.process()
            session["group"] = sel.param_groups.default # save group into session variable for reference.
            params = Parameter.query.filter(Parameter.param_group == sel.param_groups.default).paginate(1, app.config["PAGINATION_SIZE"], False) # get the currently chosen option from the select list and use to control which parameters are shown
        else:
            session["group"] = request.args.get('group', 0, type=int)

            if session["group"] > 0:
                page = request.args.get('page', 1, type=int)
                # set the session variable to the arg GROUP from the URL and then choose the params from that group id.
                sel.param_groups.default = session["group"]
                sel.process()
                params = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.id == session["group"]).first().id).paginate(page, app.config["PAGINATION_SIZE"], False)
            else:
                # Just get the first in the list as the chosen option, then get the params for that id.
                params = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.param_group == 0).first().id).paginate(1, app.config["PAGINATION_SIZE"], False)
                session["group"] = Parameter.query.filter(Parameter.param_group==0).order_by(Parameter.param_name.asc()).first().id
                sel.param_groups.default = session["group"]
                sel.process()

        return render_template("parameters.html", data=params, sel=sel)
    else:
        return render_template("403.html", error = "You are not an administrator")


# Edit Parameter for the application
@login_required
@gui_blueprint.route("/admin/editparameter/<id>", methods=["GET","POST"])
def _editparameter (id):
    if is_admin():

        param = Parameter.query.filter_by(id=id).first()
        form = ParameterForm(obj=param)

        if request.method == "GET":
            return render_template("editparameter.html", data=param, form=form)

        if form.validate_on_submit():
            if form.savebtn.data:
                if not param:
                    param = Parameter(form.id.data, form.param_name.data, form.param_value.data, form.param_group.data, form.param_parent.data, form.param_disabled.data, form.param_critical.data)
                    db.session.add(param)

                form.populate_obj(param)
                db.session.commit()
                return redirect(url_for('gui_blueprint._parameters', group=session["group"]))

            if form.deletebtn.data:
                param = Parameter.query.filter_by(id=id).first()
                capacity = Parameter.query.filter(Parameter.param_group==param.id).count()
                if capacity == 0:
                    db.session.delete(param)
                    db.session.commit()
                else:
                    flash("Cannot delete non-empty Parameter Group: " + param.param_name, "warning")

                return redirect(url_for('gui_blueprint._parameters', group=0))

        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print (fieldName + " " + err + " value:(" + str(form.param_group.data) + ")")
            return render_template("400.html", error = form.errors)

    else:
        return render_template("403.html", error = "You are not an administrator")


#################################################################
# PROFILE #
###########
@gui_blueprint.route("/editprofile", methods=["POST","GET"])
def _editprofile ():

    # Get user's details to be edited
    profile = User.query.filter(User.login_id == get_user()).first()
    form = UserForm(obj=profile)

    # If we are GET'ing the form then add data and show correct form & template
    if request.method == "GET":
        return render_template("profile.html", data=profile, form=form)

    # If we are POST'ing then we are making a change, so show message
    if form.validate_on_submit():
        if form.savebtn.data:
            try:
                profile.forename = request.form["forename"]
                profile.surname = request.form["surname"]
                profile.email = request.form["email"]
                profile.comment = request.form["comment"]
                profile.vendor = request.form["vendor"]
                db.session.commit()
                flash ("Saved Profile Details", 'success')
            except:
                flash ("Profile Not Saved", 'warning')

        return render_template("profile.html", data=profile, form=form)

#################################################################
# EMAIL #
#########

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
