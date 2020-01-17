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
    login_id = StringField('Login ID', validators=[DataRequired()])
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    comment = TextAreaField('Comment')
    password = PasswordField('Password')
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    vendor = SelectField('Vendor', coerce=int, validators=[DataRequired()])
    created_date = HiddenField('Created', default=datetime.now())
    last_login = HiddenField('Last login')
    last_modified = HiddenField('Last modified')
    modified_by = HiddenField('Modified by')
    enabled = HiddenField('Enabled', default=1)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(a.id, a.role_name) for a in Role.query.order_by(Role.role_name)]
        self.vendor.choices = [(a.id, a.param_value) for a in Parameter.query.filter(Parameter.param_group == 63).order_by(Parameter.param_name)]
        self.comment.render_kw = {'style': 'resize:none;'}

class RoleForm(FlaskForm):
    id = HiddenField('id', default=0)
    role_name = StringField('Role Name', validators=[DataRequired()])
    role_admin = SelectField('Administrator', coerce=int, default=0)
    role_app_sections = TextAreaField('Sections')
    created_date = StringField('Created')
    enabled = SelectField('Enabled', coerce=int, default=0)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.role_admin.choices = [(1, 'Yes'), (0, 'No')]
        self.enabled.choices = [(1, 'Yes'), (0, 'No')]
        self.role_app_sections.render_kw = {'disabled': True}
        self.created_date.render_kw = {'disabled': True}

class ChangeProfileForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    change_name = StringField('change_name', validators=[DataRequired()])


class ZoneForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    zone_name = SelectField('change_name', validators=[DataRequired()])


class JobForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    job_name = StringField('job_name', validators=[DataRequired()])
    job_type = SelectField('job_type', coerce=int, validators=[DataRequired()])
    job_start = StringField('job_start', validators=[DataRequired()])
    job_complete = StringField('job_complete', validators=[DataRequired()])
    job_content = TextAreaField('job_content', validators=[DataRequired()])


class ParameterForm(FlaskForm):
    id = HiddenField('id', default=0)
    param_name = StringField('Name', validators=[DataRequired()])
    param_value = TextAreaField('Value', validators=[DataRequired()])
    param_group = NoValidateSelectfield('Group', coerce=int, default=0)
    param_parent = StringField('Parent')
    param_disabled = SelectField('Disabled', coerce=int, default=0)
    param_critical = SelectField('Critical', coerce=int, default=0)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete')

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
    doi_name = StringField('Name', validators=[DataRequired()])
    doi_priority = SelectField('Priority', coerce=int)
    doi_comment = TextAreaField('Comment')
    doi_start_dt = StringField('Start', validators=[DataRequired()])
    doi_end_dt = StringField('End', validators=[DataRequired()])
    doi_regions = SelectMultipleField2('Regions')
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete')

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
    complex_name = StringField('Name', validators=[DataRequired()])
    complex_manager = SelectField('Manager', coerce=int, validators=[DataRequired()])
    complex_fw_inner_1 = StringField('Inner 1', validators=[DataRequired()])
    complex_fw_inner_2 = StringField('Inner 2', validators=[DataRequired()])
    complex_fw_outer_1 = StringField('Outer 1', validators=[DataRequired()])
    complex_fw_outer_2 = StringField('Outer 2', validators=[DataRequired()])
    complex_fw_location_1 = StringField('FW Location 1', validators=[DataRequired()])
    complex_fw_location_2 = StringField('FW Location 2', validators=[DataRequired()])
    complex_fw_type = SelectField('Firewall Type', coerce=int, validators=[DataRequired()])
    complex_serial = StringField('Serial #', validators=[DataRequired()])
    complex_license = StringField('License #', validators=[DataRequired()])
    complex_push_start = StringField('Push Start', validators=[DataRequired()])
    complex_push_end = StringField('Push End', validators=[DataRequired()])
    complex_push_days = StringField('Push Days', validators=[DataRequired()])
    complex_category = StringField('Category', validators=[DataRequired()])
    complex_hardware = StringField('Hardware', validators=[DataRequired()])
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
    complex_allow_slot_start = StringField('Slot Start')
    complex_allow_slot_end = StringField('Slot End')
    complex_push_day_extra = StringField('Extra Push Days')
    complex_change_info = StringField('Change Info')
    complex_environment = SelectField('Environment', coerce=int)
    complex_updated = StringField('Updated', render_kw={'readonly':'true'})
    complex_active = SelectField('Active', coerce=int)
    savebtn = SubmitField('Save')
    deletebtn = SubmitField('Delete')

    def __init__(self, *args, **kwargs):
        super(ComplexForm, self).__init__(*args, **kwargs)
        self.complex_fw_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 82).order_by(Parameter.param_name)] # Parameters for Priorities
        self.complex_manager.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 2).order_by(Parameter.param_name)] # Parameters for FW Managers
        self.complex_type.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 100).order_by(Parameter.param_name)] # Parameters for FW Types
        self.complex_area.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Locations
        self.complex_country.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 1).order_by(Parameter.param_value.asc())] # Parameters for Countries
        self.complex_restricted.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 105).order_by(Parameter.param_value.asc())] # Parameters for Restricted as Yes/No
        self.complex_environment.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 92).order_by(Parameter.param_value.asc())] # Parameters for Environments
        self.complex_active.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 66).order_by(Parameter.param_value.asc())] # Parameters for Active state
