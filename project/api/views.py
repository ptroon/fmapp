from flask import Flask, Blueprint, url_for, jsonify
from flask_restplus import Api, Resource, reqparse
from flask_login import login_required, login_user, logout_user, current_user

from project.models import User

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/fpa/api")
api = Api(api_blueprint, version = "1.0", \
      title = "Firewall Policy Automation API",
      description = "Provide access to FortiManagers via an API")

nsp = api.namespace('v1', description='Firewall Policy Automation APIs v1')
nsp2 = api.namespace('v2', description='Firewall Policy Automation APIs v2')

#
# ENDPOINTS
#
@nsp.route("/users")
class _users(Resource):

    def get(self):
        if not current_user.is_authenticated:
            return {"message":"Not authenticated"}
        return {"message":"Authenticated"}

    @login_required
    def post(self):
        return {"message": "Posted to Users Route"}

@nsp.route("/fortimanagers")
class _fortimanagers(Resource):
    def get(self):
        return {"message":"fortimanagers route"}

@nsp.route("/changes")
class _changes(Resource):
    def get(self):
        return "Changes route"

@nsp.route("/roles")
class _roles(Resource):
    def get(self):
        return "Roles route"

#
# AUTHENTICATION
#

rparser = api.parser()
rparser.add_argument('login_id', type=str, required=True)
rparser.add_argument('password', type=str, required=True)

@nsp.route("/session")
class _auth(Resource):
    @api.expect(rparser)
    def post(self):
        args = rparser.parse_args(strict=True)
        user = User.query.filter_by(login_id=args['login_id']).first()
        if user and user.is_correct_password(args['password']):
            login_user(user)
            return jsonify(message = "Logged in as " + current_user.forename)
        else:
            return jsonify(message = "User not found")

    def delete(self):
        if current_user.is_authenticated:
            user = current_user.login_id
            logout_user()
            return jsonify(message = "User " + user + " logged out")
        else:
            return jsonify(message = "Not currently logged in")
