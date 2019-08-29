#
# Contains the FLASK_WTF forms
#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    login_id = StringField('login_id', validators=[DataRequired()])


class ChangeProfileForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    change_name = StringField('change_name', validators=[DataRequired()])
