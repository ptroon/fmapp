
#
# Blueprint for the GUI
#

from flask import Flask, Blueprint, url_for, jsonify, make_response, app, \
        render_template, request, session, redirect, flash, g
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
import re
import logging
from datetime import datetime
from file_read_backwards import FileReadBackwards
import itertools

from sqlalchemy.orm import aliased
from sqlalchemy.orm.session import make_transient
from sqlalchemy import or_
from sqlalchemy.sql.expression import cast
from sqlalchemy import Integer as sqlInteger, String as sqlString

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
@gui_blueprint.route("/", methods=["GET"])
def _index ():

    if current_user.is_authenticated:

        a = aliased(Booking)
        b = aliased(Complex)
        c = aliased(Parameter)

        flag = request.args.get("date_select", "14")
        form = DateViewForm()

        if flag=="14":
            # Get next two weeks
            d1 = datetime.now() - timedelta(days=1)
            d2 = d1 + timedelta(days=14)

        if flag=="28":
            # Get next 4 weeks
            d1 = datetime.now() - timedelta(days=1)
            d2 = d1 + timedelta(days=28)

        if flag=="-28":
            # Get last 4 weeks
            d1 = datetime.now() - timedelta(days=28)
            d2 = d1 + timedelta(days=29)

        if flag=="0":
            d1 = datetime.now() - timedelta(weeks=52)
            d2 = datetime.now() + timedelta(weeks=52)

        admin_ = db.session.query(a, b).join(b, a.complex==b.id).\
        filter(((a.start_dt.between(d1, d2)) | \
        (a.end_dt.between(d1, d2))) | \
        ((a.start_dt < d1) & (d2 < a.end_dt))).all()

        book_ = db.session.query(a, b).join(b, a.complex==b.id).\
        filter(a.owner_id.ilike(get_user())).\
        filter(((a.start_dt.between(d1, d2)) | \
        (a.end_dt.between(d1, d2))) | \
        ((a.start_dt < d1) & (d2 < a.end_dt))).all()

        return render_template("dashboard.html", admin=admin_, book=book_, form=form, flag=flag)
    else:
        return redirect(url_for('gui_blueprint._login'))

#################################################################
# LOGIN #
#########
@gui_blueprint.route("/login", methods=["POST","GET"])
def _login ():

    form = UserForm()
    motd = Parameter.query.filter_by(id=124).first()

    if request.method=='POST':

        if request.form['login_id'] and request.form['password']:
            user = User.query.filter_by(login_id=request.form['login_id']).first()
            if not user:
                app.logger.warning ("Log in error for " + request.form['login_id'] + ", no account found")
                flash('No account found for ' + request.form['login_id'], 'warning')
                return render_template("login.html", form=form, motd=motd)
            else:
                role = Role.query.filter_by(id=user.role).first()
                _role = re.search("LOGIN", role.role_app_sections)
                if user.is_correct_password(request.form['password']) and _role: # check hash OK and user can actually log in
                    session['login_id'] = request.form['login_id']

                    # update the LAST_LOGIN field
                    user.last_login = datetime.now()
                    db.session.commit()

                    # Log in user
                    login_user(user)

                    # log this
                    app.logger.info ("Successfully logged in " + request.form['login_id'])

            if current_user.is_authenticated:
                flash('You were successfully logged in', 'success')
                if request.form.get("next", False):
                    return redirect(request.form["next"])
                return redirect(url_for('gui_blueprint._index'))

            flash('Error with login! id or password wrong or account currently locked', 'warning')
            return render_template("login.html", form=form, motd=motd), 401

        else:
            flash('Login or password missing!', 'warning')
            return render_template("login.html", form=form, motd=motd)

    else:
        return render_template("login.html", form=form, motd=motd)

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
    form.role.data = 6 # Add as a new user
    if request.method == 'GET':
        return render_template("register.html", form=form)

    if form.validate_on_submit():

        user = User.query.filter(User.login_id.ilike(form.login_id.data)).first()
        if user:
            print (model_as_dict(user))
            flash ('Error, account already exists for login "{}"'.format(user.login_id), 'warning')
            return render_template("register.html", form=form)

        user = User(form.login_id.data, form.forename.data, form.surname.data, form.comment.data, form.password.data, form.email.data, form.role.data, form.vendor.data)
        db.session.add(user)

        if not form.password.data:
            del form.password

        form.populate_obj(user)
        user.last_modified = datetime.now()
        user.modified_by = session["login_id"]
        user.last_login = None

        if not form.created_date.data:
            user.created_date = datetime.now()

        db.session.commit()
        flash ('User details registered successfully, please wait for a member of the team to contact you with your login details.', 'success')
        return redirect(url_for('gui_blueprint._index'))

    else:
        flash_errors(form)
        return render_template("register.html", form=form)


#################################################################
# COMPLEXES #
#############
@gui_blueprint.route("/admin/complexes")
@login_required
def _complexes ():
    if is_admin():

        a = aliased(Parameter)
        b = aliased(Parameter)
        c = aliased(Parameter)
        d = aliased(Parameter)

        complexes = db.session.query(Complex, a, b, c, d).\
        filter(Complex.complex_manager==a.id).\
        filter(Complex.complex_type==b.id).\
        filter(Complex.complex_country==c.id).\
        filter(Complex.complex_active==d.id).all()

        return render_template("complexes.html", data = complexes)
    else:
        return render_template("403.html", error = "You are not an administrator")

@gui_blueprint.route("/admin/editcomplex/<id>", methods=["GET","POST"])
@login_required
def _editcomplex (id):
    if is_admin():

        complex = Complex.query.filter_by(id=id).first()
        form = ComplexForm(obj=complex)

        if request.method == "GET":
            return render_template("editcomplex.html", data=complex, form=form)

        if form.validate_on_submit():
            if not complex:
                complex = Complex()
                db.session.add(complex)

            form.populate_obj(complex)
            complex.complex_updated = datetime.now()
            db.session.commit()
            flash ('Complex saved successfully', 'success')
            return redirect(url_for('gui_blueprint._complexes'))
        else:
            flash_errors(form)

        return render_template("editcomplex.html", data=complex, form=form)

    else:
        return render_template("403.html", error = "You are not an administrator")


#################################################################
# COMPLEX GROUPS #
##################

@gui_blueprint.route("/admin/complexgroups")
@login_required
def _complexgroups ():
    if is_admin():

        a = aliased(Parameter)
        b = aliased(Parameter)

        c_groups = db.session.query(ComplexGroup, a, b).\
        filter(ComplexGroup.bau_only==a.id).\
        filter(ComplexGroup.group_active==b.id).all()
        return render_template("complexgroups.html", data = c_groups)
    else:
        return render_template("403.html", error = "You are not an administrator")

@gui_blueprint.route("/admin/editcomplexgroup/<id>", methods=["GET","POST"])
@login_required
def _editcomplexgroup (id):
    if is_admin():

        c_groups = ComplexGroup.query.filter_by(id=id).first()
        form = ComplexGroupForm(obj=c_groups)

        if request.method == "GET":
            return render_template("editcomplexgroup.html", data=c_groups, form=form)

        if form.validate_on_submit():
            if not c_groups:
                c_groups = ComplexGroup()
                db.session.add(c_groups)

            form.populate_obj(c_groups)
            if not form.group_created.data:
                c_groups.group_created = datetime.now()
            db.session.commit()
            flash ('Complex Group saved successfully', 'success')
            return redirect(url_for('gui_blueprint._complexgroups'))
        else:
            flash_errors(form)

        return render_template("editcomplexgroup.html", data=c_groups, form=form)

    else:
        return render_template("403.html", error = "You are not an administrator")

#################################################################
# LOGS #
########
@gui_blueprint.route("/admin/logs", methods=["GET","POST"])
@login_required
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
@gui_blueprint.route("/admin/users", methods=["GET"])
@login_required
def _users ():
    if is_admin():
        users = db.session.query(User,Role,Parameter).join(Role).outerjoin(Parameter).order_by(User.id.asc())
        return render_template("users.html", data = users)
    else:
        return render_template("403.html", error = "You are not an administrator")

@gui_blueprint.route("/admin/edituser/<id>", methods=["GET","POST"])
@login_required
def _edituser (id):
    if is_admin():

        user = User.query.filter_by(id=id).first()
        form = UserForm(obj=user)

        if request.method == "GET":
            return render_template("edituser.html", data=user, form=form)

        if form.validate_on_submit():

            if form.savebtn.data:
                if not user:
                    user = User(form.login_id.data, form.forename.data, form.surname.data, form.comment.data, form.password.data, form.email.data, form.role.data, form.vendor.data)
                    user.last_login = None
                    db.session.add(user)

                form.populate_obj(user)
                user.last_modified = datetime.now()
                user.modified_by = session["login_id"]

                if not form.created_date.data:
                    user.created_date = datetime.now()

                db.session.commit()
                flash ('User saved successfully', 'success')
                return redirect(url_for('gui_blueprint._users'))

            if form.deletebtn.data:
                user = User.query.filter_by(id=id).first()
                db.session.delete(user)
                flash ('User removed successfully', 'success')
                db.session.commit()
                return redirect(url_for('gui_blueprint._users'))

        else:
            flash_errors (form)

        return render_template("edituser.html", data=user, form=form)

    else:
        return render_template("403.html", error = "You are not an administrator")

#################################################################
# ROLES #
#########
@gui_blueprint.route("/admin/roles", methods=["GET"])
@login_required
def _roles ():
    if is_admin():
        roles = Role.query.order_by(Role.id.asc())
        return render_template("roles.html", data = roles)
    else:
        return render_template("403.html", error = "You are not an administrator")


@gui_blueprint.route("/admin/editrole/<id>", methods=["GET","POST"])
@login_required
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
                role.created_date = datetime.now()
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

        else:
            flash_errors (form)
            return render_template("editrole.html", form=form, data=role)

        return redirect(url_for('gui_blueprint._roles'))

#################################################################
# DATES #
#########
@gui_blueprint.route("/admin/dates", methods=["GET"])
@login_required
def _dates ():
    if is_admin():
        a = aliased(Parameter)
        b = aliased(Parameter)
        c = aliased(Parameter)
        d = aliased(DateOfInterest)

        flag = request.args.get("date_select", "14")
        form = DateViewForm()

        if flag=="14":
            # Get next two weeks
            d1 = datetime.now()
            d2 = d1 + timedelta(days=14)

        if flag=="28":
            # Get next 4 weeks
            d1 = datetime.now()
            d2 = d1 + timedelta(days=28)

        if flag=="-28":
            # Get last 4 weeks
            d1 = datetime.now() - timedelta(days=28)
            d2 = d1 + timedelta(days=28)

        if flag=="0":
            d1 = datetime.now() - timedelta(weeks=52)
            d2 = datetime.now() + timedelta(weeks=52)


        dates_ = db.session.query(d.id, d.doi_name, d.doi_regions, d.doi_start_dt, d.doi_end_dt, a.param_value.label("priority"), \
        b.param_name.label("hap"), c.param_name.label("type")).join(a, d.doi_priority==a.id).\
        join(b, d.doi_hap==b.id).join(c, d.doi_type==c.id).\
        filter(((d.doi_start_dt.between(d1, d2)) | \
        (d.doi_end_dt.between(d1, d2))) | \
        ((d.doi_start_dt < d1) & (d2 < d.doi_end_dt))).all()

        dates = list(map(lambda x: x._asdict(), dates_))
        return render_template("dates.html", data=dates, form=form, flag=flag)

    else:
        return render_template("403.html", error = "You are not an administrator")


@gui_blueprint.route("/admin/editdate/<id>", methods=["GET","POST"])
@login_required
def _editdate (id):

    if is_admin():

        doi = DateOfInterest.query.filter_by(id=id).first()
        form = DOIForm(obj=doi)

        if not form.doi_filter.data:
            form.doi_filter.data = 0

        if request.method == "GET":
            if doi:
                form.doi_start_dt.data = datetime.strftime(datetime.strptime(doi.doi_start_dt, '%Y-%m-%d %H:%M:%S'), '%d/%m/%Y %H:%M')
                form.doi_end_dt.data = datetime.strftime(datetime.strptime(doi.doi_end_dt, '%Y-%m-%d %H:%M:%S'), '%d/%m/%Y %H:%M')
            return render_template("editdate.html", form=form, data=doi)

        if form.deletebtn.data:
            doi = DateOfInterest.query.filter_by(id=id).first()
            db.session.delete(doi)
            flash ('Date removed successfully', 'success')
            db.session.commit()
            return redirect(url_for('gui_blueprint._dates'))

        if form.validate_on_submit():

            start_dt = datetime.strptime(form.doi_start_dt.data, '%d/%m/%Y %H:%M')
            end_dt = datetime.strptime(form.doi_end_dt.data, '%d/%m/%Y %H:%M')

            if form.savebtn.data:
                if not doi:
                    doi = DateOfInterest(form.doi_name.data, form.doi_priority.data, form.doi_comment.data, \
                    start_dt, end_dt, form.doi_regions, form.doi_type, form.doi_filter, form.doi_hap)
                    db.session.add(doi)

                # if the type is not BAU then set to 0 as the complex group is pointless otherwise.
                if form.doi_type.data != 131:
                    form.doi_filter.data = 0

                form.populate_obj(doi)
                doi.doi_start_dt = start_dt
                doi.doi_end_dt = end_dt
                db.session.commit()

                flash ('Date saved successfully', 'success')
                return redirect(url_for('gui_blueprint._dates'))

        else:
            flash_errors(form)
            return render_template("editdate.html", form=form, data=doi)

        return redirect(url_for('gui_blueprint._dates'))


    else:
        return render_template("403.html", error = "You are not an administrator")


@gui_blueprint.route("/admin/copydate/<id>", methods=["GET","POST"])
@login_required
def _copydate (id):

    ######################
    # Inner function to copy the event with ID until date = DTE
    def copy_event(vobj, vdate):
        new_doi = vobj                  # Copy object
        db.session.expunge(new_doi)     # expunge the new object from session
        make_transient(new_doi)         # Make it transient to mark it as a "new" object
        new_doi.id  = 0                 # This is a new record now, so init ID to zero

        # Use the new date DD-MM-YYY and append the existing time HH:MM:SS
        new_sdate = vdate + " " + str(vobj.doi_start_dt).split(' ')[1]
        new_edate = vdate + " " + str(vobj.doi_end_dt).split(' ')[1]
        new_doi.doi_start_dt = datetime.strptime(new_sdate, '%d/%m/%Y %H:%M:%S')
        new_doi.doi_end_dt   = datetime.strptime(new_edate, '%d/%m/%Y %H:%M:%S')

        print (str(new_doi.doi_start_dt) + " " + str(new_doi.doi_end_dt))

        # return object
        return new_doi
    ######################


    form=CopyDateForm(id=id)

    if request.method == "GET":

        a = aliased(DateOfInterest)
        c = aliased(Parameter)
        d = aliased(Parameter)
        f = aliased(ComplexGroup)

        event = db.session.query(a, c, d, func.fmapp.rem_slots(a.id).label("slotsAvailable"), f).\
        join(c, a.doi_type==c.id).join(d, a.doi_priority==d.id).\
        outerjoin(f, a.doi_filter==f.id).filter(a.id==int(id)).first()

        form.event_name.data = event[0].doi_name # cache the name

        return render_template("copydate.html", event=event, form=form)

    if request.method == "POST":

        if not form.end_date.data:
            flash("No date given so copy not completed for '" + form.event_name.data + "'", "info") # No date provided, so show this
        else:

            doi = DateOfInterest.query.filter_by(id=id).first()
            try:
                if form.copy_select.data == '1':  # Option to copy to that date ONLY
                    db.session.add(copy_event (doi, form.end_date.data))

                if form.copy_select.data in ['7', '14', '28']: # Copy X times to that date
                    date_ = datetime.strptime(doi.doi_start_dt, '%Y-%m-%d %H:%M:%S')
                    end_ =  datetime.strptime(form.end_date.data, '%d/%m/%Y')
                    vdays = int(form.copy_select.data)
                    while date_ <= end_:
                        date_ = date_ + timedelta(days=vdays)
                        db.session.add(copy_event (doi, date_.strftime('%d/%m/%Y')))
                        db.session.flush()

                db.session.commit()

            except Exception as e:
                    flash("Copy failed because " + str(e), "danger") # Copy was a success
                    return redirect(url_for('gui_blueprint._dates')) # Back to the main Dates page


            flash("Copy completed for " + form.event_name.data, "success") # Copy was a success

        return redirect(url_for('gui_blueprint._dates')) # Back to the main Dates page

#################################################################
# SEARCH #
##########
@gui_blueprint.route("/search", methods=["GET","POST"])
def _search ():

    a = aliased(DateOfInterest)
    b = aliased(Booking)

    form = MainSearchForm()
    if request.method == 'POST':

        # get query
        query = request.form.get('search_input', None)

        if query:

            ####################################################################
            # DATES
            conditions = []
            for qry in query.split(" "):
                conditions.append((a.doi_comment+' '+a.doi_name).ilike(('%{}%').format(qry)))

            results1 = db.session.query(a.id, a.doi_name.label("name"), a.doi_comment.label("description"), \
            a.doi_start_dt.label("start"), a.doi_end_dt.label("end")).\
            filter(or_(*conditions)).all()

            ####################################################################
            # BOOKINGS
            conditions = []
            for qry in query.split(" "):
                conditions.append((b.description).ilike(('%{}%').format(qry)))
                conditions.append((b.title).ilike(('%{}%').format(qry)))
                conditions.append((b.change_ref).ilike(('%{}%').format(qry)))
                conditions.append((b.change_subref).ilike(('%{}%').format(qry)))
                conditions.append((b.stakeholder_id).ilike(('%{}%').format(qry)))

            results2 = db.session.query(b.id, b.title.label("name"), b.description, \
            b.start_dt.label("start"), b.end_dt.label("end")).\
            filter(or_(*conditions)).all()

            results = []
            results.extend(results1)
            results.extend(results2)

            return render_template("search.html", query=query, results=results, form=form)
        else:
            return render_template("search.html", query=None, results=None, form=form)
    else:
        return render_template("search.html", query=None, results=None, form=form)

#################################################################
# HELP #
########
@gui_blueprint.route("/usage")
def _help ():

    if request.method == 'GET':
        help = db.session.query(Parameter.param_name, Parameter.param_value).filter(Parameter.param_group==113).order_by(Parameter.id.asc()).all()
        return render_template("help.html", data = help)

#################################################################
# BOOKINGS #
############

@gui_blueprint.route("/bookings", methods=["GET"])
def _bookings ():

    # Show the booking calendar view
    if request.method == "GET":
        form = ComplexNameSelectForm()
        defdate = request.args.get("defdate", datetime.now())
        return render_template("calendar.html", form=form, defdate=defdate)


# This is waaaayy too long!!
@gui_blueprint.route("/editbooking/<int:id>", defaults={'evt': 0}, methods=["GET","POST"])
@gui_blueprint.route("/editbooking/<int:id>/<int:evt>", methods=["GET","POST"])
def _editbooking (id, evt):

    #for key, value in request.form.items():
    #    print(key, value)

    booking = Booking.query.filter_by(id=id).first()
    form = BookingForm(obj=booking)
    event = DateOfInterest.query.filter(DateOfInterest.id==int(form.slot_id.data)).first()

    if request.method == "GET" and request.referrer:
        complex = Complex.query.filter(Complex.id==int(form.complex.data)).first() # Get complex object from query
        event = DateOfInterest.query.filter(DateOfInterest.id==int(form.slot_id.data)).first()

        form.tmp_date.data = datetime.strptime(form.start_dt.data.split()[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        form.tmp_start_t.data = form.start_dt.data.split()[1]
        form.tmp_end_t.data = form.end_dt.data.split()[1]
        form.complex_text.data = complex.complex_name
        flash_errors(form)
        return render_template("editbooking.html", form=form, event=event)


    if request.method == "POST":

        if request.form.get("deletebtn", False):
            db.session.delete(booking)
            db.session.commit()
            flash("Booking deleted successfully", 'success')
            return redirect(url_for('gui_blueprint._index'))

        # check from initial select form submitted as "Next"
        if request.form.get("nextbtn", False):
            cplx = int(request.form.get("complex_select", 1)) # Get Complex ID
            complex = Complex.query.filter(Complex.id==int(cplx)).first() # Get complex object from query
            event = DateOfInterest.query.filter(DateOfInterest.id==evt).first()
            print (event.doi_name)

            s_time = complex.complex_push_start
            e_time = complex.complex_push_end
            form.start_dt.default = request.form.get("start") + " " + s_time
            form.end_dt.default = request.form.get("start") + " " + e_time
            form.tmp_date.default = request.form.get("start").replace("-","/")
            form.tmp_start_t.default = s_time
            form.tmp_end_t.default = e_time
            form.slot_id.default = evt
            form.owner_id.data = get_user()

            if is_day_allowed(request.form.get("start"), complex.complex_push_days):
                form.approval_required.default = "0" # may change once the booking has been checked
            else:
                form.approval_required.default = "1"

            form.complex.default = request.form.get("complex_select", 1)
            form.complex_text.default = complex.complex_name

            form.process()
            return render_template("editbooking.html", form=form, event=event)

        # This is the actual booking page and we're trying to save the record
        # VALID
        if form.validate_on_submit():

            # We have made it to the process/checking section.  Data is valid so we determine if the booking
            # needs to be approved or not.  Bookings are always saved, but either as auto-approved or pending approval
            if request.form.get("checkbtn", False):
                db.session.autoflush = False
                complex = Complex.query.filter(Complex.id==int(form.complex.data)).first() # Get complex object from query

                if not booking: # this is a new record
                    booking = Booking()
                    db.session.add(booking)

                form.populate_obj(booking)
                booking.start_dt = datetime.strptime(form.start_dt.data, '%d-%m-%Y %H:%M')
                booking.end_dt = datetime.strptime(form.end_dt.data, '%d-%m-%Y %H:%M')
                booking.logged = datetime.now()

                # Check the booking meets the rules set out in the system for auto approvals
                # Does the booking meet the core rules?
                flag_core = is_booking_core_ok(form.tmp_date.data, form.complex.data)

                # Does this deviate from the standard day/time combination in the complex record?
                flag_cust = is_booking_custom(form.tmp_start_t.data, form.tmp_end_t.data, form.complex.data)

                # Does the booking have an approval flag already set?
                flag_reqd = (str(form.approval_required.data) != '1')

                flag_bau = (int(form.slot_id.data) <= 0)

                if flag_core and not flag_cust and flag_reqd and flag_bau:

                    booking.approved_date = datetime.now()
                    booking.approved_by = 'Automatic Approval'
                    booking.approval_reason = booking.approved_by
                    flash ('Booking was saved and automatically approved', 'success')

                else:
                    # The booking will be saved, but pending approval
                    del booking.approved_date
                    del booking.approved_by

                    booking.approval_reason = 'Booking pending'

                    if not flag_core:
                        booking.approval_reason += ', too many bookings per day/complex)'
                    if flag_cust or not flag_reqd:
                        booking.approval_reason += ', non-standard start/end times requested'
                    if not flag_bau:
                        booking.approval_reason += ', BaU bookings require manual approval'

                    flash ('Booking was saved but is pending approval by the Operations team', 'warning')

                db.session.autoflush = True
                db.session.commit()

            # we are just saving the record
            if request.form.get("savebtn", False):

                try:
                    form.start_dt.data = datetime.strptime(form.tmp_date.data + " " + form.tmp_start_t.data, '%d-%m-%Y %H:%M')
                    form.end_dt.data = datetime.strptime(form.tmp_date.data + " " + form.tmp_end_t.data, '%d-%m-%Y %H:%M')
                except:
                    pass

                form.populate_obj(booking)
                db.session.commit()

            return redirect(url_for('gui_blueprint._index'))

        # INVALID, so go back to edit page and get corrections by user.
        else:
            flash_errors(form)
            return render_template("editbooking.html", form=form)


#################################################################
# APPROVE BOOKIMG #
###################
# Toggle approved state for a booking
@gui_blueprint.route("/approvebooking/<id>", methods=["GET"])
@login_required
def _approvebooking (id):

    if is_admin():
        booking = Booking.query.filter_by(id=id).first()
        if booking.approved_date:
            booking.approved_date = None
            booking.approved_by = None
            booking.approval_reason = "Manually set to not approved by " + get_user()
        else:
            booking.approved_date = datetime.now()
            booking.approved_by = get_user()
            booking.approval_reason = "Approved by " + get_user()
        flash("Toggled approval date for booking <{}>".format(booking.title))
        db.session.commit()
    else:
        flash ("Cannot toggle booking approval unless an administrator")

    return redirect(url_for('gui_blueprint._index'))

#################################################################
# PUSH DAYS #
#############
@gui_blueprint.route("/pushdays", methods=["GET"])
def _pushdays ():

    cplx_list = []
    a_cplx = []

    if request.method == "GET":

        search = request.args.get('search', None) # see if a search argument was given

        complexes = Complex.query.filter(Complex.complex_active==67).all() # get all complexes that are ACTIVE

        # put complexes into a list of lists, with inner list containing the specific complex details
        # and the outer list containing a list of all complexes
        for cplx in complexes:
            a_cplx.append(cplx.complex_name)
            for day_ in cplx.complex_push_days:
                a_cplx.append(day_)
            cplx_list.append(a_cplx)
            a_cplx = []

        return render_template("push.html", data=cplx_list, search=search)

#################################################################
# COMMUNICATIONS #
##################
@gui_blueprint.route("/admin/comms", methods=["GET","POST"])
@login_required
def _comms ():

    if is_admin():
        form = CommsOptionsSelectForm()

        if request.method == 'GET':
            form.date_picker.data = datetime.now().strftime("%d/%m%Y")
            return render_template("comms.html", form=form)

        if request.method == 'POST':
            type_ = request.form.get("type_select", 0)
            emails = Parameter.query.filter(Parameter.param_name.like("OPERATIONS_EMAILS")).first()
            content = Parameter.query.filter(Parameter.param_parent==type_).first()
            return render_template("comms.html", form=form, emails=emails, content=content)

    else:
        return render_template("403.html", error = "You are not an administrator")

#################################################################
# PARAMETERS #
##############
# Show parameters in a form using a select box to control groupings
@gui_blueprint.route("/admin/parameters", methods=["GET","POST"])
@login_required
def _parameters ():

    if is_admin():
        sel = ParameterSearchForm()

        if request.method == 'POST':
            sel.param_groups.default = request.form["param_groups"]
            sel.process()
            session["group"] = sel.param_groups.default # save group into session variable for reference.
            # params = Parameter.query.filter(Parameter.param_group == sel.param_groups.default).paginate(1, app.config["PAGINATION_SIZE"], False) # get the currently chosen option from the select list and use to control which parameters are shown
            params = Parameter.query.filter(Parameter.param_group == sel.param_groups.default).all()
        else:
            session["group"] = request.args.get('group', 0, type=int)

            if session["group"] > 0:
                page = request.args.get('page', 1, type=int)
                # set the session variable to the arg GROUP from the URL and then choose the params from that group id.
                sel.param_groups.default = session["group"]
                sel.process()
                # params = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.id == session["group"]).first().id).paginate(page, app.config["PAGINATION_SIZE"], False)
                params = Parameter.query.filter(Parameter.param_group == Parameter.query.filter(Parameter.id == session["group"]).first().id).all()
            else:
                # Just get the first in the list as the chosen option, then get the params for that id.
                session["group"] = Parameter.query.filter(Parameter.param_group==0).order_by(Parameter.param_name.asc()).first().id
                # params = Parameter.query.filter(Parameter.param_group == session["group"]).paginate(1, app.config["PAGINATION_SIZE"], False)
                params = Parameter.query.filter(Parameter.param_group == session["group"]).all()
                sel.param_groups.default = session["group"]
                sel.process()

        return render_template("parameters.html", data=params, sel=sel)
    else:
        return render_template("403.html", error = "You are not an administrator")


# Edit Parameter for the application
@gui_blueprint.route("/admin/editparameter/<id>", methods=["GET","POST"])
@login_required
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
@gui_blueprint.route("/editprofile", methods=["GET","POST"])
@login_required
def _editprofile ():

    # Get user's details to be edited
    profile = User.query.filter(User.login_id == get_user()).first()
    form = UserForm(obj=profile)

    # If we are GET'ing the form then add data and show correct form & template
    if request.method == "GET":
        return render_template("profile.html", data=profile, form=form)

    del form.role # user can't change this in their profile
    del form.last_login # they aren't logging in at this stage

    # If we are POST'ing then we are making a change, so show message
    if form.validate_on_submit():
        if form.savebtn.data:

            # delete password if they haven't entered text to change it.
            if not form.password.data:
                del form.password

            form.populate_obj(profile)
            profile.last_modified = datetime.now()
            profile.modified_by = session["login_id"]
            db.session.commit()
            flash ("Saved Profile Details", 'success')
            return redirect(url_for('gui_blueprint._index'))

    else:
        flash_errors(form)
        return render_template("profile.html", data=profile, form=form)

#################################################################
# SHOW EVENT BOOKING MODALS #
#############################
@gui_blueprint.route("/showdate", defaults={'dte': 0}, methods=["GET","POST"])
@gui_blueprint.route("/showdate/<string:dte>", methods=["GET","POST"])
@login_required
def _showdate (dte):

    d1 = datetime.strptime(dte, '%d-%m-%Y')
    d2 = d1 + timedelta(minutes=1439)
    locked_flag = 0

    a = aliased(DateOfInterest)

    doi_ = db.session.query(a.id, a.doi_name, a.doi_start_dt, a.doi_end_dt, a.doi_comment, a.doi_type).\
    filter(((a.doi_start_dt.between(d1, d2)) | \
    (a.doi_end_dt.between(d1, d2))) | \
    ((a.doi_start_dt < d1) & (d2 < a.doi_end_dt))).all()

    # set the result set as a list with column names
    res = list(map(lambda x: x._asdict(), doi_))
    # get the count for locked events.
    locked_flag = len(list(filter(lambda item: item['doi_type'] == 130, res)))

    return render_template("eventinfo.html", dte=dte, events=res, locked_flag=locked_flag)

# Non-BaU Bookings form giving all complexes
@gui_blueprint.route("/showdate/book/<string:dte>", methods=["GET","POST"])
@login_required
def _showdate_book (dte):

    form = ComplexNameSelectForm()
    return render_template("eventbook.html", dte=dte, form=form)

# Show BAU Event and allow booking a slot
@gui_blueprint.route("/showdate/bau/<string:dte>/<int:id>", methods=["GET"])
@login_required
def _showdate_bau (dte, id):

    a = aliased(DateOfInterest)
    b = aliased(Booking)
    c = aliased(ComplexGroup)
    d = aliased(Complex)

    events_ = db.session.query(a.id, a.doi_name, a.doi_start_dt, a.doi_end_dt, a.doi_comment, a.doi_type).filter(a.id==id).all()
    events = list(map(lambda x: x._asdict(), events_))

    bookings_ = db.session.query(b.id, b.slot_id, b.title, b.ticket, b.owner_id, b.approved_date).\
    filter(cast(b.slot_id, sqlInteger)==id).all()
    bookings = list(map(lambda x: x._asdict(), bookings_))

    form = ComplexGroupNameSelectForm()
    choices = db.session.query(c.id, c.group_name).join(a, a.doi_filter==c.id).filter(a.id==id).all()
    form.group_select.choices = choices

    # get the members field for the specified group and turn it into a list
    members = db.session.query(c.group_members).filter(c.id==choices[0][0]).all()
    cplxs = db.session.query(d.id, d.complex_name).filter(d.id.in_(members[0][0].split(','))).all()
    form.complex_select.choices = cplxs

    slots = db.session.query(c.max_slots).filter(c.id==choices[0][0]).first()
    form.max_slots.data = slots.max_slots

    return render_template("eventbau.html", dte=dte, id=id, events=events, bookings=bookings, form=form)

# Entry point for viewing events
@gui_blueprint.route("/showevent/<string:dte>/<string:evt>/<int:id>", methods=["GET"])
@login_required
def _showevent (dte, evt, id):

    a = aliased(DateOfInterest)
    b = aliased(Booking)
    c = aliased(Parameter)
    d = aliased(Parameter)
    e = aliased(Complex)

    if evt == "DATE":
        event_ = db.session.query(a, c, d).join(c, a.doi_type==c.id).join(d, a.doi_priority==d.id).filter(a.id==int(id)).all()

        if event_[0][0].doi_type == 131:
            # go to the BaU booking page
            return redirect(url_for('gui_blueprint._showdate_bau', dte=dte, id=id))
        # Got to the Event Review page
        return render_template("eventreview.html", dte=dte, event=event_[0])

    if evt == "BOOKING":
        book_ = db.session.query(b,e).join(e, b.complex==e.id).filter(b.id==int(id)).all()

        # Got to the Event Review page
        return render_template("eventreview.html", dte=dte, book=book_[0])

    return "Error: /<Date>/DATE|BOOKING/<Id>"

# Provides the text for a tooltip of the specified event by taking the id/type and giving a web page
@gui_blueprint.route("/showttip/<int:id>/<string:evt>", methods=["GET"])
@login_required
def _showttip (id, evt):

    a = aliased(DateOfInterest)
    b = aliased(Booking)
    c = aliased(Parameter)
    d = aliased(Parameter)
    e = aliased(Complex)
    f = aliased(ComplexGroup)

    if evt == "DATE":
        event = db.session.query(a, c, d, func.fmapp.rem_slots(a.id).label("slotsAvailable"), f).\
        join(c, a.doi_type==c.id).join(d, a.doi_priority==d.id).\
        outerjoin(f, a.doi_filter==f.id).filter(a.id==int(id)).first()
        return render_template("showttip.html", event=event)

    if evt == "BOOKING":
        book = db.session.query(b,e).join(e, b.complex==e.id).filter(b.id==int(id)).first()
        return render_template("showttip.html", book=book)


#################################################################
# EMAIL #
#########
'''
@gui_blueprint.route("/admin/email", methods=["POST","GET"])
@login_required
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
'''
