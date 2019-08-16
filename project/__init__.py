from flask import Flask, Blueprint, url_for, jsonify
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from project.instance.config import app_config, current_config
from project.api.views import api_blueprint

#
# TBC
# Use Flask DispatcherMiddleware to combine API and GUI apps into one
#

app = Flask(__name__, instance_relative_config=True)          
app.config.from_object(app_config[current_config])

db = SQLAlchemy(app)
app.register_blueprint(api_blueprint)
