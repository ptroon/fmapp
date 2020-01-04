#
# Contains the FLASK_WTF forms
#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

from project.models import *

class UserForm(FlaskForm):
    id = HiddenField('id', default=0)
    login_id = StringField('Login ID', validators=[DataRequired()])
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    comment = TextAreaField('Comment')
    password = PasswordField('Password')
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    created_date = HiddenField('Created', default=datetime.now())
    last_login = HiddenField('Last login')
    last_modified = HiddenField('Last modified')
    modified_by = HiddenField('Modified by')
    enabled = HiddenField('Enabled', default=1)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(a.id, a.role_name) for a in Role.query.order_by(Role.role_name)]


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
    param_value = StringField('Value', validators=[DataRequired()])
    param_group = SelectField('Group', coerce=int, default=0)
    param_parent = StringField('Parent')
    param_disabled = SelectField('Disabled', coerce=int, default=0)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.param_disabled.choices = [(1, 'Yes'), (0, 'No')]
        self.param_group.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 0).order_by(Parameter.param_group)]
        self.param_parent.render_kw = {'disabled': True}

class ParameterSearchForm(FlaskForm):
    param_groups = SelectField('Groups', coerce=int)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ParameterSearchForm, self).__init__(*args, **kwargs)
        self.param_groups.choices = [(a.id, a.param_name) for a in Parameter.query.filter(Parameter.param_group == 0).order_by(Parameter.param_group)]
