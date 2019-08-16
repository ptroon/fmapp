from flask import Flask, Blueprint, url_for
from flask_restplus import Api, Resource

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
        return {"message":"Users route"}

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
@nsp.route("/authenticate")
class _auth(Resource):
    def get(self):
        return "LOGIN route"
    def delete(self):
        return "LOGOUT route"
