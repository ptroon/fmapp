#
# Contains the FLASK_WTF forms
#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField, TextAreaField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    id = HiddenField('id')
    login_id = StringField('Login ID', validators=[DataRequired()])
    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    comment = TextAreaField('Comment')
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = IntegerField('Role')
    created_date = StringField('Created')
    last_login = StringField('Last login')
    last_modified = StringField('Last modified')
    modified_by = StringField('Modified by')
    enabled = StringField('Enabled', validators=[DataRequired()])

class ChangeProfileForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    change_name = StringField('change_name', validators=[DataRequired()])
