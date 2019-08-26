from flask import Flask, Blueprint, url_for, jsonify, abort
from flask_restplus import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from project.instance.config import app_config, current_config

#
# TBC
# Use Flask DispatcherMiddleware to combine API and GUI apps into one
#

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

print(app.url_map)

#
#
from project.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
