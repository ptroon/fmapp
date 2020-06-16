from flask import Flask, Blueprint, url_for, jsonify, abort, session, render_template, request, flash
from flask_restplus import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

from project.instance.config import app_config, current_config

#
# TBC
# Use Flask DispatcherMiddleware to combine API and GUI apps into one (Q1 2020)
#

#################################################################
# HELPER functions for Jinja2 #
###############################
# Gets the application name from the config file
def get_name():
    return app.config["APP_NAME"]

# Gets the application version from the config file
def get_version():
    return app.config["VERSION"]

# Gets the application copyright message from the config file
def get_copyright():
    return app.config["COPYRIGHT"]

# Gets the user LOGIN_ID
def get_user():
    return session.get("login_id", "Anonymous") # return "Anon" user if no key found

def unique_time():
    return "?=" + str(datetime.utcnow()).replace(" ","")

def get_now(fmt):
    if fmt=="S":
        return datetime.now().strftime('%d-%m-%Y')
    if fmt=="M":
        return datetime.now().strftime('%B %d %Y - %H:%M:%S')
    if fmt=="L":
        return datetime.now().strftime('%B %d %Y - %H:%M:%S')
    if fmt=='UTC':
        return datetime.utcnow()

def is_earlier(dte):
    try:
        d1 = datetime.strptime(dte, '%d-%m-%Y')
    except Exception as e:
        print (e)
        return False

    if get_now('UTC') <= d1:
        return True
    else:
        return False


# Check if the current user is in an admin flagged role and if yes, return True to show the admin menu
def is_admin():
    user = User.query.filter_by(login_id=get_user()).join(Role, User.role==Role.id).filter_by(role_admin=1).first()
    if user:
        return True
    return False

def test_null(var):
    try:
        if var is None:
            return True;
        if len(var)==0:
            return True;
        else:
            return False
    except:
        return True

#################################################################
# SET-UP APP #
##############

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[current_config])

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
mail = Mail(app)

@app.before_request
def before_request():
    pass

#################################################################
# LOGGING #
###########

logging.basicConfig(filename = app.config["LOG_FILE"], level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db_logger = logging.getLogger('sqlalchemy.engine')
db_handler = TimedRotatingFileHandler(app.config["DB_LOG_FILE"], when='midnight', backupCount=10)
db_logger.setLevel(logging.DEBUG)
db_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'))
db_logger.addHandler(db_handler)
logging.getLogger('sqlalchemy.pool').addHandler(db_handler)
logging.getLogger('sqlalchemy').propagate = False

#################################################################
# LOGIN MANAGEMENT #
####################

login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    return abort(403)

#################################################################
# BLUEPRINTS #
##############
from project.api.views import api_blueprint
from project.gui.views import gui_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(gui_blueprint)

'''
if app.config["ENV"] == 'development':
    print(app.url_map)
'''

#
# Delayed import & register LOAD_USER function for FLASK_LOGIN
from project.models import User, Role

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# Register the functions so Jinja can call them from templates
app.jinja_env.globals.update(get_name=get_name)
app.jinja_env.globals.update(get_version=get_version)
app.jinja_env.globals.update(get_user=get_user)
app.jinja_env.globals.update(is_admin=is_admin)
app.jinja_env.globals.update(unique_time=unique_time)
app.jinja_env.globals.update(get_copyright=get_copyright)
app.jinja_env.globals.update(test_null=test_null)
app.jinja_env.globals.update(get_now=get_now)
app.jinja_env.globals.update(is_earlier=is_earlier)

login_manager.blueprint_login_views = { 'gui_blueprint' : '/fpa/login', 'api_blueprint' : '/fpa/login', }
login_manager.needs_refresh_message = (u"Session timedout, please login again")
login_manager.needs_refresh_message_category = "info"
login_manager.refresh_view = '/fpa/login'

# Default 404 Error handler
@app.errorhandler(404)
def not_found (e):
    return render_template("404.html", error=e, error_url=request.path)

# Default 403 Error handler
@app.errorhandler(403)
def not_found (e):
    flash (e, "warning")
    return render_template("login.html", next=request.path)
