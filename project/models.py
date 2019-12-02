#
# Contains the MODEL information for the database
#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from flask_login import UserMixin
from cryptography.fernet import Fernet

from project import db, bcrypt, app

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

class FortiManager(db.Model):

    __tablename__ = "fortimanagers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_name = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String(32), nullable=False)
    adom_mode = db.Column(db.Integer, default=0)
    serial = db.Column(db.String(32))
    version = db.Column(db.String(64))
    username = db.Column(db.String(64), nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    sync_time = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0)

    def __init__(self, host_name, ip, username, plaintext_password):
        self.host_name = host_name
        self.ip = ip
        self.username = username
        self.password = plaintext_password
        self.adom_mode = 0
        self.serial = None
        self.version = None
        self.sync_time = None
        self.status = None

    @hybrid_property
    def password(self):
        f = Fernet(app.config["CRYPTO_KEY"])
        return f.decrypt(self._password.encode()).decode()

    @password.setter
    def password(self, plaintext_password):
        f = Fernet(app.config["CRYPTO_KEY"])
        self._password = f.encrypt(plaintext_password.encode())

class ChangeProfile(db.Model):

    __tablename__ = "change_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    change_name = db.Column(db.String(256))
    change_desc = db.Column(db.Text)
    master_record = db.Column(db.String(32))
    task_record = db.Column(db.String(32))
    sbid = db.Column(db.String(9))
    budget_code = db.Column(db.String(32))
    target_date = db.Column(db.DateTime)
    change_raiser = db.Column(db.Integer)
    change_checker = db.Column(db.Integer)
    change_approver = db.Column(db.Integer)
    change_implementer = db.Column(db.Integer)
    change_raised = db.Column(db.DateTime)
    change_checked = db.Column(db.DateTime)
    change_approved = db.Column(db.DateTime)
    change_implemented = db.Column(db.DateTime)

    def __init__(self, change_name, change_desc, master_record, task_record, sbid, budget_code, target_date, change_raiser):
        self.change_name = change_name
        self.change_desc = change_desc
        self.master_record = master_record
        self.task_record = task_record
        self.sbid = sbid
        self.budget_code = budget_code
        self.target_date = target_date
        self.change_raiser = change_raiser


class Dashboard(db.Model):

    __tablename__ = "dashboard"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fm_text = db.Column(db.Text)
    fg_text = db.Column(db.Text)
    user_text = db.Column(db.Text)
    log_text = db.Column(db.Text)

    def __init__(self, fm, fg, user, log):
        self.fm_text = fm
        self.fg_text = fg
        self.user_text = user
        self.log_text = log

class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    url = db.Column(db.String(1000))
    logged = db.Column(db.DateTime)
    owner_id = db.Column(db.String(25))
    zone = db.Column(db.String(200))
    approved_date = db.Column(db.DateTime)
    approved_by = db.Column(db.String(32))

    def __init__(self):
        self.logged = datetime.now()


class Complex(db.Model):

    __tablename__ = "complexes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    complex_name = db.Column(db.String(1000), nullable=False)
    complex_mgr = db.Column(db.String(1000), nullable=False)
    complex_type = db.Column(db.String(1000), nullable=False)
    firewall_type = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(1000), nullable=False)
    environment = db.Column(db.String(1000), nullable=False)
    updated = db.Column(db.String(1000), nullable=False)
    active = db.Column(db.String(1000), nullable=False)

class Parameter(db.Model):

    __tablename__ = "parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    param_name = db.Column(db.String(1000), nullable=False)
    param_value = db.Column(db.String(2000), nullable=False)
    param_parent = db.Column(db.Integer)
