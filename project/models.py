#
# Contains the MODEL information for the database
#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from flask_login import UserMixin
from cryptography.fernet import Fernet
from sqlalchemy import inspect

from project import db, bcrypt, app


# creates a Dict from a db.Model
def model_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

# Custom DateTime type because Python Datetime is a PitA
class DateTime2(db.TypeDecorator):
    impl = db.DateTime

    # prep for saving to database
    def process_bind_param(self, value, dialect):
        if type(value) is str:
            if len(value) > 0: # prevent null string error
                return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            else:
                return None
        return value

    # prep for extraction from database into form fields
    def process_result_value(self, value, dialect):
        if type(value) is datetime:
            return datetime.strftime(value, '%Y-%m-%d %H:%M:%S')

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
    vendor = db.Column(db.Integer, db.ForeignKey("parameters.id"))
    created_date = db.Column(DateTime2)
    last_login = db.Column(DateTime2)
    last_modified = db.Column(DateTime2)
    modified_by = db.Column(db.String(100))
    enabled = db.Column(db.Integer)

    def __init__(self, login_id, forename, surname, comment, plaintext_password, email, role, vendor):
        self.login_id = login_id
        self.forename = forename
        self.surname = surname
        self.comment = comment
        self.password = plaintext_password
        self.email = email
        self.role = role
        self.vendor = vendor
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

    @hybrid_property
    def created_date_str(self):
        return datetime.strftime(self.created_date, '%d-%m-%Y %H:%M')

class Role(db.Model, UserMixin):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), nullable=False)
    role_admin = db.Column(db.Integer, nullable=False)
    role_app_sections = db.Column(db.String(200))
    created_date = db.Column(DateTime2, nullable=False)
    enabled = db.Column(db.Integer)

    def __init__(self, role_name, role_admin, role_app_sections, enabled):
        self.role_name = role_name
        self.role_admin = role_admin
        self.role_app_sections = role_app_sections
        self.created_date = datetime.now()
        self.enabled = enabled

class FortiManager(db.Model, UserMixin):

    __tablename__ = "fortimanagers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_name = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String(32), nullable=False)
    adom_mode = db.Column(db.Integer, default=0)
    serial = db.Column(db.String(32))
    version = db.Column(db.String(64))
    username = db.Column(db.String(64), nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    sync_time = db.Column(DateTime2)
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

class ChangeProfile(db.Model, UserMixin):

    __tablename__ = "change_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    change_name = db.Column(db.String(256))
    change_desc = db.Column(db.Text)
    master_record = db.Column(db.String(32))
    task_record = db.Column(db.String(32))
    sbid = db.Column(db.String(9))
    budget_code = db.Column(db.String(32))
    target_date = db.Column(DateTime2)
    change_raiser = db.Column(db.Integer)
    change_checker = db.Column(db.Integer)
    change_approver = db.Column(db.Integer)
    change_implementer = db.Column(db.Integer)
    change_raised = db.Column(DateTime2)
    change_checked = db.Column(DateTime2)
    change_approved = db.Column(DateTime2)
    change_implemented = db.Column(DateTime2)

    def __init__(self, change_name, change_desc, master_record, task_record, sbid, budget_code, target_date, change_raiser):
        self.change_name = change_name
        self.change_desc = change_desc
        self.master_record = master_record
        self.task_record = task_record
        self.sbid = sbid
        self.budget_code = budget_code
        self.target_date = target_date
        self.change_raiser = change_raiser


class Dashboard(db.Model, UserMixin):

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


class Parameter(db.Model, UserMixin):

    __tablename__ = "parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    param_name = db.Column(db.String(1000), nullable=False)
    param_value = db.Column(db.String(2000), nullable=False)
    param_group = db.Column(db.Integer)
    param_parent = db.Column(db.Integer)
    param_disabled = db.Column(db.Integer)
    param_critical = db.Column(db.Integer)

    def __init__(self, id, p_name, p_value, p_group, p_parent, p_disabled, p_critical):
        self.id = id
        self.param_name = p_name
        self.param_value = p_value
        self.param_group = p_group
        self.param_disabled = p_disabled
        self.param_parent = p_parent
        self.param_critical = p_critical


class Job(db.Model, UserMixin):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name = db.Column(db.String(1000), nullable=False)
    job_type = db.Column(db.Integer, nullable=False)
    job_start = db.Column(DateTime2, nullable=False)
    job_complete = db.Column(DateTime2)
    job_content = db.Column(db.String(4000), nullable=False)


class DateOfInterest(db.Model, UserMixin):

    __tablename__ = "datesofinterest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doi_name = db.Column(db.String(1000), nullable=False)
    doi_priority = db.Column(db.Integer, db.ForeignKey("parameters.id"), default=0, nullable=False)
    doi_comment = db.Column(db.String(2000))
    doi_start_dt = db.Column(DateTime2, nullable=False)
    doi_end_dt = db.Column(DateTime2, nullable=False)
    doi_regions = db.Column(db.String(100))
    doi_locked = db.Column(db.Integer, default=0)
    doi_hap = db.Column(db.Integer, default=0)

    def __init__(self, doi_name, doi_priority, doi_comment, doi_start_dt, doi_end_dt, doi_regions, doi_locked, doi_hap):
        self.doi_name = doi_name
        self.doi_priority = doi_priority
        self.doi_comment = doi_comment
        self.doi_start_dt = doi_start_dt
        self.doi_end_dt = doi_end_dt
        self.doi_regions = doi_regions
        self.doi_locked = doi_locked
        self.doi_hap = doi_hap

'''
    @hybrid_property
    def doi_regions_ms(self):
        return self.doi_regions.split(',') # provides a list

    @doi_regions_ms.setter
    def doi_regions_ms(self, _doi_regions):
        self.doi_regions = ','.join(_doi_regions) # creates a comma delimited string
'''

class Complex(db.Model, UserMixin):

    __tablename__ = "complexes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    complex_name = db.Column(db.String(1000), db.ForeignKey("parameters.id"), nullable=False)
    complex_manager = db.Column(db.Integer, db.ForeignKey("parameters.id"), nullable=False)
    complex_fw_inner_1 = db.Column(db.String(1000))
    complex_fw_inner_2 = db.Column(db.String(1000))
    complex_fw_outer_1 = db.Column(db.String(1000))
    complex_fw_outer_2 = db.Column(db.String(1000))
    complex_fw_location_1 = db.Column(db.String(1000))
    complex_fw_location_2 = db.Column(db.String(1000))
    complex_fw_type = db.Column(db.Integer, db.ForeignKey("parameters.id"), nullable=False)
    complex_serial = db.Column(db.String(1000), default='N/A')
    complex_license = db.Column(db.String(1000), default='N/A')
    complex_push_start = db.Column(db.Integer, nullable=False)
    complex_push_end = db.Column(db.Integer, nullable=False)
    complex_push_days = db.Column(db.String(7), default="NNNNNNN")
    complex_category = db.Column(db.String(1000))
    complex_hardware = db.Column(db.String(1000))
    complex_fw_inner_name_1 = db.Column(db.String(1000))
    complex_fw_inner_name_2 = db.Column(db.String(1000))
    complex_location_1 = db.Column(db.String(1000))
    complex_fw_outer_name_1 = db.Column(db.String(1000))
    complex_fw_outer_name_2 = db.Column(db.String(1000))
    complex_location_2 = db.Column(db.String(1000))
    complex_location_all = db.Column(db.String(1000))
    complex_area = db.Column(db.Integer, db.ForeignKey("parameters.id"), nullable=False)
    complex_fw_info1 = db.Column(db.String(1000))
    complex_fw_info2 = db.Column(db.String(1000))
    complex_fw_inner_info1 = db.Column(db.String(1000))
    complex_fw_inner_info2 = db.Column(db.String(1000))
    complex_fw_outer_info1 = db.Column(db.String(1000))
    complex_fw_outer_info2 = db.Column(db.String(1000))
    complex_type = db.Column(db.Integer, db.ForeignKey("parameters.id"), nullable=False)
    complex_info_1 = db.Column(db.String(1000))
    complex_country = db.Column(db.Integer, db.ForeignKey("parameters.id"), nullable=False)
    complex_restricted = db.Column(db.Integer, db.ForeignKey("parameters.id"))
    complex_restrict_start = db.Column(db.Integer)
    complex_restrict_end = db.Column(db.Integer)
    complex_allow_slot_day = db.Column(db.Integer)
    complex_allow_slot_start = db.Column(db.Integer)
    complex_allow_slot_end = db.Column(db.Integer)
    complex_push_day_extra = db.Column(db.String(7))
    complex_change_info = db.Column(db.String(2000))
    complex_environment = db.Column(db.Integer, db.ForeignKey("parameters.id"))
    complex_updated = db.Column(DateTime2, default=datetime.now())
    complex_active = db.Column(db.Integer, db.ForeignKey("parameters.id"), default=1)


class Booking(db.Model, UserMixin):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slot_id = db.Column(db.Integer)
    title = db.Column(db.String(32), nullable=False)
    start_dt = db.Column(DateTime2, nullable=False)
    end_dt = db.Column(DateTime2, nullable=False)
    ticket = db.Column(db.String(20), nullable=False)
    stakeholder_id = db.Column(db.String(20))
    budget = db.Column(db.String(20))
    project = db.Column(db.String(100))
    description = db.Column(db.String(4000), nullable=False)
    owner_id = db.Column(db.String(25))
    complex = db.Column(db.Integer)
    cluster = db.Column(db.Integer)
    approval_required = db.Column(db.Integer)
    approved_date = db.Column(DateTime2)
    approved_by = db.Column(db.String(25))
    change_ref = db.Column(db.String(20))
    change_subref = db.Column(db.String(20))
    logged = db.Column(DateTime2)


    def __init__(self, *args, **kwargs):
        self.logged = datetime.now()
        super(Booking, self).__init__()
