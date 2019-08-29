from flask import Flask, Blueprint, url_for, jsonify, abort, session
from flask_restplus import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import logging

from project.instance.config import app_config, current_config

#
# TBC
# Use Flask DispatcherMiddleware to combine API and GUI apps into one
#

# HELPER functions
##################

# Gets the application version from the config file
def get_version():
    return app.config["VERSION"]

# Gets the user LOGIN_ID
def get_user():
    return session["login_id"]

# Check if the current user is in an admin flagged role and if yes, return True to show the admin menu
def is_admin():
    user = User.query.filter_by(login_id=get_user()).join(Role, User.role==Role.id).filter_by(role_admin=1).first()
    if user:
        return True
    return False

# SET-UP
########

logging.basicConfig(filename = 'fpa.log', level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[current_config])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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

if app.config["ENV"] == 'development':
    print(app.url_map)

#
# Delayed import & register LOAD_USER function for FLASK_LOGIN
from project.models import User, Role

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

# Register the functions so Jinja can call them from templates
app.jinja_env.globals.update(get_version=get_version)
app.jinja_env.globals.update(get_user=get_user)
app.jinja_env.globals.update(is_admin=is_admin)
