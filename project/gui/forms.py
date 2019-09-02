#
# Contains the FLASK_WTF forms
#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

from project.models import Role

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
