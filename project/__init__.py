from flask import Flask, Blueprint, url_for, jsonify, abort, session, render_template
from flask_restplus import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import logging
from datetime import datetime

from project.instance.config import app_config, current_config

#
# TBC
# Use Flask DispatcherMiddleware to combine API and GUI apps into one
#

####################
# HELPER functions #
####################
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
    return session["login_id"]

def unique_time():
    return "?=" + str(datetime.utcnow()).replace(" ","")

# Check if the current user is in an admin flagged role and if yes, return True to show the admin menu
def is_admin():
    user = User.query.filter_by(login_id=get_user()).join(Role, User.role==Role.id).filter_by(role_admin=1).first()
    if user:
        return True
    return False

##########
# SET-UP #
##########

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[current_config])

logging.basicConfig(filename = app.config["LOG_FILE"], level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

login_manager = LoginManager(app)
login_manager.login_view='api_blueprint.session'

# This handles the unauthorised access requests to URIs
@login_manager.unauthorized_handler
def unauthorized():
    return abort(403)

#
# BLUEPRINTS
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


# Default 404 Error handler
@app.errorhandler(404)
def not_found (e):
    print(e)
    return render_template("404.html", error = e)
