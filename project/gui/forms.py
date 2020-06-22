#
# Contains the FLASK_WTF forms
#
from flask_wtf import FlaskForm
from flask import session
from wtforms import *
from wtforms.validators import *
from wtforms.widgets.html5 import *
from datetime import datetime
import re

from project.models import *
from project import get_user

PUSH_DAY_ERRORMSG = "Push Day must be 7 characters and use Y or N only"
PASSWORD_ERRORMSG = "Password must contain at least one numeric, alpha, upper & special char and be > 7 chars"
PASSWORD_INITIAL_ERRORMSG = "Password must be provided on new user account creation"
EMAIL_SUFFIX_ERRORMSG = "Email must have an internal suffix, cannot be external"
ENDDATE_ERRORMSG  = 'End Date must be greater than Start Date and not blank'
CHANGE_SUBREF_ERRORMSG_MISSING = 'Task must start TCR and contain 7 digits if main reference is an MCR'
CHANGE_SUBREF_ERRORMSG_NNULL = 'Task must be null if the main reference is not an MCR'
CHANGE_REF_ERRORMSG = 'Change reference must start with MCR, SCR or RCR and have 7 digits'
DUPLICATE_USER_ERRORMSG = "User already exists, please use a different Login ID"
MAX_SLOTS_ERRORMSG = "Number of slots is higher than allowed per change, less than or equal to"
DATETYPE_ERRORMSG = "If Date type is 'BaU' then you must have a complex group chosen"
DATEREF_ERRORMSG = "If Date type is 'BaU' then you must enter an MCR/SCR reference"
###############################################################################
# OVERIDES #
############

class NoValidateSelectfield(SelectField):
    def pre_validate(self, form):
        None

class SelectMultipleField2(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

    def process_data(self, value):
        if not value:
            self.data = []
        else:
            try:
                self.data = value.split(',')

            except (ValueError, TypeError):
                self.data = []


###############################################################################
# FORMS #
#########

class UserForm(FlaskForm):
    id = HiddenField('id', default=0)
    login_id = StringField('Login ID', validators=[InputRequired()])
    forename = StringField('Forename', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    comment = TextAreaField('Comment')
    password = PasswordField('Password')
    email = StringField('Email')
    role = NoValidateSelectfield('Role', coerce=int, validators=[InputRequired()])
    vendor = SelectField('Vendor', coerce=int, validators=[InputRequired()])
    created_date = HiddenField('Created')
    last_login = HiddenField('Last login')
    last_modified = HiddenField('Last modified')
    modified_by = HiddenField('Modified by')
    enabled = HiddenField('Enabled', default=1)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(a.id, a.role_name) for a in Role.query.order_by(Role.role_name)]
        self.vendor.choices = [(a.id, a.param_value) for a in Parameter.query.filter(Parameter.param_group == 63).order_by(Parameter.param_name)]
        self.comment.render_kw = {'style': 'resize:none;'}

    def validate_email(form, field):
        # get the email regexp validation parameter
        rex = Parameter.query.filter(Parameter.id==125).first()

        if rex:
            # check the suffix using a regex
            if not re.search(rex.param_value, field.data): # check it matches or raise error
                raise ValidationError(EMAIL_SUFFIX_ERRORMSG)

    def validate_password(form, field):
        # if a new account, then check password provided
        if int(form.id.data) == 0:
            if len(field.data)<=0 or field.data is None:
                raise ValidationError(PASSWORD_INITIAL_ERRORMSG)

        # check password is valid if supplied
        if len(field.data)>0:
            if not re.match ("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", field.data):
                raise ValidationError(PASSWORD_ERRORMSG)

    def validate_login_id(form, field):
        # check for a duplicate user account.
        if int(form.id.data) == 0:
            user = User.query.filter(User.login_id==field.data).first()
            if user:
                raise ValidationError(DUPLICATE_USER_ERRORMSG)

class RoleForm(FlaskForm):
    id = HiddenField('id', default=0)
    role_name = StringField('Role Name', validators=[InputRequired()])
    role_admin = SelectField('Administrator', coerce=int, default=0)
    role_app_sections = TextAreaField('Privileges')
    created_date = StringField('Created')
    enabled = SelectField('Enabled', coerce=int, default=0)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.role_admin.choices = [(1, 'Yes'), (0, 'No')]
        self.enabled.choices = [(1, 'Yes'), (0, 'No')]
        self.role_app_sections.render_kw = {'style': 'resize:none;'}
        self.created_date.render_kw = {'disabled': True}

class ChangeProfileForm(FlaskForm):
    id = IntegerField('id', validators=[InputRequired()])
    change_name = StringField('change_name', validators=[InputRequired()])


class ZoneForm(FlaskForm):
    id = IntegerField('id', validators=[InputRequired()])
    zone_name = SelectField('change_name', validators=[InputRequired()])


class JobForm(FlaskForm):
    id = IntegerField('id', validators=[InputRequired()])
    job_name = StringField('job_name', validators=[InputRequired()])
    job_type = SelectField('job_type', coerce=int, validators=[InputRequired()])
    job_start = StringField('job_start', validators=[InputRequired()])
    job_complete = StringField('job_complete', validators=[InputRequired()])
    job_content = TextAreaField('job_content', validators=[InputRequired()])


class ParameterForm(FlaskForm):
    id = HiddenField('id', default=0)
    param_name = StringField('Name', validators=[InputRequired()])
    param_value = TextAreaField('Value', validators=[InputRequired()])
    param_group = NoValidateSelectfield('Group', coerce=int, default=0)
    param_parent = NoValidateSelectfield('Parent', coerce=int, default=0)
    param_disabled = SelectField('Disabled', coerce=int, default=0)
    param_critical = SelectField('Critical', coerce=int, default=0)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.param_disabled.choices = [(1, 'Yes'), (0, 'No')]
        self.param_group.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 0).order_by(Parameter.param_name)]
        # Add the 'zero' option into the choices list
        select_option = self.param_group.choices
        self.param_group.choices = [('0', '-- Top Level Group --')] + select_option
        self.param_parent.render_kw = {'disabled': False}
        self.param_critical.choices = [(1, 'Yes'), (0, 'No')]
        self.param_parent.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group != 0).order_by(Parameter.param_name)]
        select_option = self.param_parent.choices
        self.param_parent.choices = [('0', '-- No Parent --')] + select_option

class ParameterSearchForm(FlaskForm):
    param_groups = SelectField('Groups', coerce=int)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ParameterSearchForm, self).__init__(*args, **kwargs)
        self.param_groups.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 0).order_by(Parameter.param_name)]

class MainSearchForm(FlaskForm):
    search_input = StringField('Query')
    search_options = SelectField('Options', coerce=int)
    search = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super(MainSearchForm, self).__init__(*args, **kwargs)
        self.search_options.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 71).order_by(Parameter.param_name)]

class LogForm(FlaskForm):
    log_options = SelectField('Options')
    log_records = SelectField('Records')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)
        self.log_options.choices = [(a.param_value, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 75).order_by(Parameter.param_name)] # Parameters for Log Types
        self.log_records.choices = [(a.param_value, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 78).order_by(Parameter.param_name)] # Parameters for Number of Records

class DateViewForm(FlaskForm):
    date_select = SelectField('DateOpts')
    submit = SubmitField('Go')

    def __init__(self, *args, **kwargs):
        super(DateViewForm, self).__init__(*args, **kwargs)
        self.date_select.choices = [(a.param_value, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 132).order_by(Parameter.param_name)] # Parameters for Date Views
        self.date_select.render_kw = {'data-style': "btn-secondary"}

class DOIForm(FlaskForm):
    id = HiddenField('id', default=0)
    doi_name = StringField('Name', validators=[InputRequired(),Length(min=5,max=40)])
    doi_priority = SelectField('Priority', coerce=int)
    doi_comment = TextAreaField('Comment')
    doi_start_dt = StringField('Start', validators=[InputRequired()])
    doi_end_dt = StringField('End', validators=[InputRequired()])
    doi_regions = SelectMultipleField2('Regions')
    doi_type = SelectField('Event Type', coerce=int)
    doi_filter = SelectField('Items', coerce=int)
    doi_environment = SelectField('Environment', coerce=int)
    doi_change_ref = StringField('Reference')
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(DOIForm, self).__init__(*args, **kwargs)
        self.doi_priority.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 82).order_by(Parameter.param_name)] # Parameters for Priorities
        self.doi_comment.render_kw = {'style': 'resize:none;'}
        self.doi_start_dt.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Choose start date & time'}
        self.doi_end_dt.render_kw = {'data-target': '#datetimepicker2', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Choose end date & time'}
        self.doi_regions.choices = [(a.param_value, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Locations
        self.doi_filter.choices = [(a.id, a.group_name) for a in ComplexGroup.query.order_by(ComplexGroup.group_name.asc())] # Parameters for Complex Groups
        select_group = self.doi_filter.choices
        self.doi_filter.choices = [(0, '-- Complex Groups --')] + select_group
        self.doi_filter.render_kw = {'data-live-search': 'true', 'class': ' form-control', 'width': 'fit', 'data-container': 'body'}
        self.doi_regions.render_kw = {'multiple': 'true'}
        self.doi_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 127).filter(Parameter.param_disabled==0).order_by(Parameter.param_name)] # Event Types
        self.doi_environment.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 92).filter(Parameter.param_disabled==0).order_by(Parameter.param_name)] # Environments
        select_group = self.doi_environment.choices
        self.doi_environment.choices = [(0, 'All Environments')] + select_group
        self.doi_environment.render_kw = {'title': 'Pick the environment this applies to'}
        self.doi_type.render_kw = {"title": "The event type required"}
        self.doi_change_ref.render_kw = {"title": "Enter the MCR or SCR ref"}

    def validate_doi_end_dt(form, field):
        if datetime.strptime(field.data, '%d/%m/%Y %H:%M') <= datetime.strptime(form.doi_start_dt.data, '%d/%m/%Y %H:%M'):
            raise ValidationError(ENDDATE_ERRORMSG)

    def validate_doi_filter(form, field):
        if (form.doi_type.data == 131 and field.data == 0):
            raise ValidationError(DATETYPE_ERRORMSG)

    def validate_doi_change_ref(form, field):
        if (form.doi_type.data == 131 and field.data == ""):
            raise ValidationError(DATEREF_ERRORMSG)

class ComplexForm(FlaskForm):
    id = HiddenField('id', default=0)
    complex_name = StringField('Name', validators=[InputRequired()])
    complex_manager = SelectField('Manager', coerce=int, validators=[InputRequired()])
    complex_fw_inner_1 = StringField('Inner 1', validators=[InputRequired()])
    complex_fw_inner_2 = StringField('Inner 2', validators=[InputRequired()])
    complex_fw_outer_1 = StringField('Outer 1', validators=[InputRequired()])
    complex_fw_outer_2 = StringField('Outer 2', validators=[InputRequired()])
    complex_fw_location_1 = StringField('FW Location 1', validators=[InputRequired()])
    complex_fw_location_2 = StringField('FW Location 2', validators=[InputRequired()])
    complex_fw_type = SelectField('Firewall Type', coerce=int, validators=[InputRequired()])
    complex_serial = StringField('Serial #', validators=[InputRequired()])
    complex_license = StringField('License #', validators=[InputRequired()])
    complex_push_start = StringField('Push Start', validators=[InputRequired()])
    complex_push_end = StringField('Push End', validators=[InputRequired()])
    complex_push_days = StringField('Push Days', validators=[InputRequired(), Regexp('^[NY]{7}$', message=PUSH_DAY_ERRORMSG)], default="NNNNNNN")
    complex_category = StringField('Category', validators=[InputRequired()])
    complex_hardware = StringField('Hardware', validators=[InputRequired()])
    complex_fw_inner_name_1 = StringField('FW Inner Name 1')
    complex_fw_inner_name_2 = StringField('FW Inner Name 2')
    complex_location_1 = StringField('Complex Location 1')
    complex_fw_outer_name_1 = StringField('FW Outer Name 1')
    complex_fw_outer_name_2 = StringField('FW Outer Name 2')
    complex_location_2 = StringField('Complex Location 2')
    complex_location_all = StringField('Location All')
    complex_area = SelectField('Area', coerce=int)
    complex_fw_info1 = StringField('FW Info 1')
    complex_fw_info2 = StringField('FW Info 2')
    complex_fw_inner_info1 = StringField('FW Inner Info 1')
    complex_fw_inner_info2 = StringField('FW Inner Info 2')
    complex_fw_outer_info1 = StringField('FW Outer Info 1')
    complex_fw_outer_info2 = StringField('FW Outer Info 2')
    complex_type = SelectField('Type', coerce=int)
    complex_info_1 = StringField('Complex Info 1')
    complex_country = SelectField('Country', coerce=int)
    complex_restricted = SelectField('Restricted', coerce=int, validators=[Optional()])
    complex_restrict_start = StringField('Restrict Start', validators=[Optional()])
    complex_restrict_end = StringField('Restrict End', validators=[Optional()])
    complex_allow_slot_day = StringField('Slot Day')
    complex_allow_slot_start = StringField('Slot Start Time')
    complex_allow_slot_end = StringField('Slot End Time')
    complex_push_day_extra = StringField('Extra Push Days', validators=[InputRequired(), Regexp('^[NY]{7}$', message=PUSH_DAY_ERRORMSG)], default="NNNNNNN")
    complex_change_info = StringField('Change Info')
    complex_environment = SelectField('Environment', coerce=int)
    complex_updated = StringField('Updated', render_kw={'readonly':'true'})
    complex_active = SelectField('Active', coerce=int)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(ComplexForm, self).__init__(*args, **kwargs)
        self.complex_fw_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 89).order_by(Parameter.param_name)] # Parameters for
        self.complex_manager.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 2).order_by(Parameter.param_name)] # Parameters for FW Managers
        self.complex_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 100).order_by(Parameter.param_name)] # Parameters for FW Types
        self.complex_area.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Locations
        self.complex_country.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Countries
        self.complex_restricted.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 105).order_by(Parameter.param_value.asc())] # Parameters for Restricted as Yes/No
        self.complex_environment.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 92).filter(Parameter.param_disabled==0).order_by(Parameter.param_value.asc())] # Parameters for Environments
        self.complex_active.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 66).order_by(Parameter.param_value.asc())] # Parameters for Active state
        self.complex_push_start.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Click to choose Start time'}
        self.complex_push_end.render_kw = {'data-target': '#datetimepicker2', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Click to choose End time'}
        self.complex_restrict_start.render_kw = {'data-target': '#datetimepicker3', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Click to choose Start date & time'}
        self.complex_restrict_end.render_kw = {'data-target': '#datetimepicker4', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Click to choose End date & time'}

    def validate_complex_restrict_end(form, field):
        if datetime.strptime(field.data, '%d/%m/%Y %H:%M') <= datetime.strptime(form.complex_restrict_start.data, '%d/%m/%Y %H:%M'):
            raise ValidationError(ENDDATE_ERRORMSG)

class ComplexGroupForm(FlaskForm):
    id = HiddenField('id', default=0)
    group_name = StringField('Name', validators=[InputRequired()])
    max_slots = IntegerField('Max slots', widget=NumberInput(min=1, max=10), validators=[InputRequired()])
    group_members = SelectMultipleField2('Complex Members')
    group_created = StringField('Created')
    bau_only = SelectField('BaU Only', coerce=int)
    group_active = SelectField('Active', coerce=int)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(ComplexGroupForm, self).__init__(*args, **kwargs)
        self.group_members.choices = [(a.id, a.complex_name) for a in Complex.query.order_by(Complex.complex_name.asc())] # Complexes
        self.group_active.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 66).order_by(Parameter.param_value.asc())] # Parameters for Active state
        self.bau_only.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 105).order_by(Parameter.param_name)] # Yes/No
        self.group_created.render_kw = {'readonly': 'true'}
        self.group_members.render_kw = {'data-live-search': 'true'}

    def validate_max_slots(form, field):
        try:
            max_s = Parameter.query.filter(Parameter.id == 126).first()
        except:
            max_s = 10
        if int(field.data) > int(max_s.param_value):
            raise ValidationError(MAX_SLOTS_ERRORMSG + " " + max_s.param_value)


class CommsOptionsSelectForm(FlaskForm):
    date_picker = StringField('Date')
    type_select = SelectField('Type')
    env_select = SelectField('Env')
    btngo = SubmitField('Go')

    def __init__(self, *args, **kwargs):
        super(CommsOptionsSelectForm, self).__init__(*args, **kwargs)
        self.type_select.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 116).order_by(Parameter.param_name)] # Comms Email Options
        self.date_picker.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Select Date to search'}
        self.env_select.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 92).filter(Parameter.param_disabled==0).order_by(Parameter.param_name)] # Environments
        select_group = self.env_select.choices
        self.env_select.choices = [(0, 'All Environments')] + select_group


class ComplexNameSelectForm(FlaskForm):
    complex_select = SelectField('Complex')
    vendor_select = SelectField('Vendor')
    nextbtn = SubmitField('Next')

    def __init__(self, *args, **kwargs):
        super(ComplexNameSelectForm, self).__init__(*args, **kwargs)
        self.complex_select.choices = [(a.id, a.complex_name) for a in Complex.query.filter(Complex.complex_environment==session["env"]).order_by(Complex.complex_name)] # Complex Names
        self.vendor_select.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 100).order_by(Parameter.param_name)] # Complex Type
        select_option = self.vendor_select.choices
        self.vendor_select.choices = [('0', '-- All Vendors --')] + select_option
        self.vendor_select.render_kw = {'onchange': 'change_vendor()'}
        self.complex_select.render_kw = {'onchange': 'change_complex()'}


class ComplexGroupNameSelectForm(FlaskForm):
    group_select = SelectField('Complex Group')
    complex_select = SelectField('Complex')
    max_slots = HiddenField('Max Slots')
    nextbtn = SubmitField('Next')

    def __init__(self, *args, **kwargs):
        super(ComplexGroupNameSelectForm, self).__init__(*args, **kwargs)
        self.group_select.choices = [(a.id, a.group_name) for a in ComplexGroup.query.order_by(ComplexGroup.group_name)] # Complex Groups
        self.complex_select.choices = [(a.id, a.complex_name) for a in Complex.query.order_by(Complex.complex_name)] # Complex Names
        self.group_select.render_kw = {'class':'form-control', 'onchange': 'change_group()'}
        self.complex_select.render_kw = {'class':'form-control','onchange': 'change_complex()'}


class CopyDateForm(FlaskForm):
    id = HiddenField("ID")
    event_name = HiddenField("Name")
    copy_select = NoValidateSelectfield('Copy Action')
    end_date = StringField('Date', validators=[InputRequired()])
    savebtn = SubmitField("Copy")

    def __init__(self, *args, **kwargs):
        super(CopyDateForm, self).__init__(*args, **kwargs)
        self.end_date.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': 'true', 'data-placement':'top', 'onchange': 'change_date()'}
        self.copy_select.choices = [(a.param_value, a.param_name) for a in Parameter.query.filter(Parameter.param_group==138).order_by(Parameter.id)] # Complex Names
        self.savebtn.render_kw = {'class': 'button_fpa btn-primary btn'}


class EnvForm(FlaskForm):
    env_select = SelectField('Environment')

    def __init__(self, *args, **kwargs):
        super(EnvForm, self).__init__(*args, **kwargs)
        self.env_select.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group==92).filter(Parameter.param_disabled==0).order_by(Parameter.param_name)] # Environments
        self.env_select.render_kw = {'onchange': 'change_env()', 'class': 'form-control-lg bg-light text-primary'}


class BookingForm(FlaskForm):
    id = HiddenField('id', default=0)
    slot_id = HiddenField('Slot', default=0)
    title = StringField('Title', validators=[InputRequired()])
    start_dt = HiddenField('Start', validators=[InputRequired()])
    end_dt = HiddenField('End', validators=[InputRequired()])
    ticket = StringField('Ticket', validators=[InputRequired(),Length(6,7)])
    stakeholder_id = StringField('Stakeholder', render_kw={"title": "Enter Stakeholder RACF"})
    budget = StringField('Budget Code')
    project = StringField('Project Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    owner_id = StringField('Owner', validators=[InputRequired()], render_kw={"title": "Booking owner/implementer RACF", "readonly":"false"})
    complex = HiddenField('Complex')
    cluster = SelectField('Cluster', coerce=int)
    approval_required = StringField('Approval Required?', render_kw={"title": "APPROVAL REQUIRED FOR THIS CHANGE DUE TO NON-STANDARD DAY OF WEEK"})
    approved_date = StringField('Approved')
    approved_by = StringField('Approved By')
    approval_reason = StringField('Approval Reason')
    change_ref = StringField('Change Ref', render_kw={"title": "Enter SCR/MCR ID"}, validators=[Regexp('^[MRS]CR[1-9]{7}$', message=CHANGE_REF_ERRORMSG)])
    change_subref = StringField('Task Ref', render_kw={"title": "Enter TCR # if main is MCR"})
    logged = HiddenField('logged')
    savebtn = SubmitField('Save')
    checkbtn = SubmitField('Check')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})
    tmp_date = StringField('Booking Date', render_kw={'readonly':'true'})
    tmp_start_t = StringField('Start Time')
    tmp_end_t = StringField('End Time')
    complex_text = StringField('Complex', render_kw={'readonly':'true'})
    tmp_hash = HiddenField('Hash Token')

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.description.render_kw = {'style': 'resize:none;'}
        self.tmp_start_t.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Click to choose start time'}
        self.tmp_end_t.render_kw = {'data-target': '#datetimepicker2', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Click to choose end time'}
        self.complex.choices = [(a.id, a.complex_name) for a in Complex.query.order_by(Complex.complex_name)] # Complex Names
        self.cluster.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 97).order_by(Parameter.param_name)] # Cluster Names
        self.owner_id.default = get_user()

    def validate_change_subref(form, field):
        if form.change_ref.data.startswith('MCR',0) and not re.match('^[T]CR[1-9]{7}$', field.data):
            raise ValidationError(CHANGE_SUBREF_ERRORMSG_MISSING)
        if re.match('^[RS]CR[1-9]{7}$', form.change_ref.data) and not re.match('^$', field.data):
            raise ValidationError(CHANGE_SUBREF_ERRORMSG_NNULL)

    def validate_tmp_start_t(form, field):
        if field.data > form.tmp_end_t.data:
            raise ValidationError(ENDDATE_ERRORMSG)
