#
# Contains the FLASK_WTF forms
#
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import datetime

from project.models import *

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
    email = StringField('Email', validators=[InputRequired(), Email()])
    role = SelectField('Role', coerce=int, validators=[InputRequired()])
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

class RoleForm(FlaskForm):
    id = HiddenField('id', default=0)
    role_name = StringField('Role Name', validators=[InputRequired()])
    role_admin = SelectField('Administrator', coerce=int, default=0)
    role_app_sections = TextAreaField('Sections')
    created_date = StringField('Created')
    enabled = SelectField('Enabled', coerce=int, default=0)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.role_admin.choices = [(1, 'Yes'), (0, 'No')]
        self.enabled.choices = [(1, 'Yes'), (0, 'No')]
        self.role_app_sections.render_kw = {'disabled': True}
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
    param_parent = StringField('Parent')
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
        self.param_parent.render_kw = {'disabled': True}
        self.param_critical.choices = [(1, 'Yes'), (0, 'No')]

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

class DOIForm(FlaskForm):
    id = HiddenField('id', default=0)
    doi_name = StringField('Name', validators=[InputRequired()])
    doi_priority = SelectField('Priority', coerce=int)
    doi_comment = TextAreaField('Comment')
    doi_start_dt = StringField('Start', validators=[InputRequired()])
    doi_end_dt = StringField('End', validators=[InputRequired()])
    doi_regions = SelectMultipleField2('Regions')
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(DOIForm, self).__init__(*args, **kwargs)
        self.doi_priority.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 82).order_by(Parameter.param_name)] # Parameters for Priorities
        self.doi_comment.render_kw = {'style': 'resize:none;'}
        self.doi_start_dt.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Choose start date & time'}
        self.doi_end_dt.render_kw = {'data-target': '#datetimepicker2', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Choose end date & time'}
        self.doi_regions.choices = [(a.param_value, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Locations
        self.doi_regions.render_kw = {'multiple': 'true'}

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
    complex_push_days = StringField('Push Days', validators=[InputRequired()])
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
    complex_restricted = SelectField('Restricted', coerce=int)
    complex_restrict_start = StringField('Restrict Start')
    complex_restrict_end = StringField('Restrict End')
    complex_allow_slot_day = StringField('Slot Day')
    complex_allow_slot_start = StringField('Slot Start Time')
    complex_allow_slot_end = StringField('Slot End Time')
    complex_push_day_extra = StringField('Extra Push Days', validators=[InputRequired()])
    complex_change_info = StringField('Change Info')
    complex_environment = SelectField('Environment', coerce=int)
    complex_updated = StringField('Updated', render_kw={'readonly':'true'})
    complex_active = SelectField('Active', coerce=int)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(ComplexForm, self).__init__(*args, **kwargs)
        self.complex_fw_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 89).order_by(Parameter.param_name)] # Parameters for Priorities
        self.complex_manager.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 2).order_by(Parameter.param_name)] # Parameters for FW Managers
        self.complex_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 100).order_by(Parameter.param_name)] # Parameters for FW Types
        self.complex_area.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Locations
        self.complex_country.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Countries
        self.complex_restricted.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 105).order_by(Parameter.param_value.asc())] # Parameters for Restricted as Yes/No
        self.complex_environment.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 92).order_by(Parameter.param_value.asc())] # Parameters for Environments
        self.complex_active.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 66).order_by(Parameter.param_value.asc())] # Parameters for Active state

    def validate_complex_push_day_extra(form, field):
        if len(field.data) != 7:
            raise ValidationError('Push Days must be exactly 7 characters')


class ComplexNameSelectForm(FlaskForm):
    complex_select = SelectField('Complex')
    nextbtn = SubmitField('Next')

    def __init__(self, *args, **kwargs):
        super(ComplexNameSelectForm, self).__init__(*args, **kwargs)
        self.complex_select.choices = [(a.id, a.complex_name) for a in Complex.query.order_by(Complex.complex_name)] # Complex Names


class BookingForm(FlaskForm):
    id = HiddenField('id', default=0)
    slot_id = HiddenField('slot_id', default=0)
    title = StringField('Title', validators=[InputRequired()])
    start_dt = StringField('Start', validators=[InputRequired()])
    end_dt = StringField('End', validators=[InputRequired()])
    ticket = StringField('Ticket', validators=[InputRequired(),Length(6,7)])
    stakeholder_id = StringField('Stakeholder')
    budget = StringField('Budget Code')
    project = StringField('Project Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    owner_id = StringField('Owner', validators=[InputRequired()])
    complex = NoValidateSelectfield('Complex', coerce=int, render_kw={'disabled':'true'})
    cluster = NoValidateSelectfield('Cluster', coerce=int)
    approved_date = StringField('Approved')
    approved_by = StringField('Approved By')
    change_ref = StringField('Change Ref')
    change_subref = StringField('Change Sub Ref')
    logged = HiddenField('logged')
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete', render_kw={'hidden':'true'})

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.description.render_kw = {'style': 'resize:none;'}
        self.start_dt.render_kw = {'data-target': '#datetimepicker1', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Choose start date & time'}
        self.end_dt.render_kw = {'data-target': '#datetimepicker2', 'data-toggle': 'datetimepicker', 'readonly': '', 'data-placement':'top', 'title':'Choose end date & time'}
        self.complex.choices = [(a.id, a.complex_name) for a in Complex.query.order_by(Complex.complex_name)] # Complex Names
        self.cluster.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 97).order_by(Parameter.param_name)] # Cluster Names
