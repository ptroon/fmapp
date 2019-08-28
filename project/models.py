#
# Contains the MODEL information for the database
#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from flask_login import UserMixin

from project import db, bcrypt

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_id = db.Column(db.String(25), unique=True, nullable=False)
    forename = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(2000))
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("roles.id"))
    created_date = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    modified_by = db.Column(db.String(100))
    enabled = db.Column(db.Integer)

    def __init__(self, login_id, forename, surname, comment, plaintext_password, email, role):
        self.login_id = login_id
        self.forename = forename
        self.surname = surname
        self.comment = comment
        self.password = plaintext_password
        self.email = email
        self.role = role
        self.created_date = datetime.now()
        self.last_login = None
        self.last_modified = None
        self.modified_by = None
        self.enabled = 0

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

class Role(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), nullable=False)
    role_admin = db.Column(db.Integer, nullable=False)
    role_app_sections = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, nullable=False)
    enabled = db.Column(db.Integer)

    def __init__(self, role_name, role_admin, role_app_sections):
        self.role_name = role_name
        self.role_admin = role_admin
        self.role_app_sections = role_app_sections
        self.created_date = datetime.now()
        self.deleted = 0
