#
# Contains the MODEL information for the database
#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from project import db, bcrypt

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_id = db.Column(db.String, nullable=False)
    forename = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    modified_by = db.Column(db.String)
    deleted = db.Column(db.Integer)

    def __init__(self, login_id, forename, surname, plaintext_password, email, role):
        self.login_id = login_id
        self.forename = forename
        self.surname = surname
        self.password = plaintext_password
        self.email = email
        self.role = role
        self.created_date = datetime.now()
        self.last_login = None
        self.last_modified = None
        self.modified_by = None
        self.deleted = 0

'''
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext_password):
        #self._password = bcrypt.generate_password_hash(plaintext_password)
        self._password = plaintext_password
'''
