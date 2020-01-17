from flask import Flask, Blueprint, url_for, jsonify, make_response
from flask_restplus import Api, Resource, reqparse
from flask_login import login_required, login_user, logout_user, current_user
from itsdangerous import JSONWebSignatureSerializer

from project.models import *
from project import app, db, is_admin, mail, get_user
from project.gui.forms import *
from project.gui.logic import *

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/fpa/api")
api = Api(api_blueprint, version = "1.0", \
      title = "Firewall Policy Automation API",
      description = "Provide access to FortiManagers via an API")

nsp = api.namespace('v1', description='Firewall Policy Automation APIs v1')
nsp2 = api.namespace('v2', description='Firewall Policy Automation APIs v2')

#
# ENDPOINTS
#
@login_required
@nsp.route("/users")
class _users(Resource):
    def get(self):
        if is_admin():
            users = db.session.query(User,Role,Parameter).join(Role).outerjoin(Parameter).order_by(User.id.asc())
            return users

@nsp.route("/roles")
class _fortimanagers(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {"message":"fortimanagers route"}
        return {"message":"not logged in for Fortimanagers route"}

@nsp.route("/dates")
class _changes(Resource):
    def get(self):
        return "Changes route"

@nsp.route("/complexes")
class _roles(Resource):
    def get(self):
        return "Roles route"

'''
@nsp.route("/bookings")
class _bookings(Resource):
    def get(self):
        month_name = request.args.get('month', '')
        booking = Booking.query().all()
'''

#
# AUTHENTICATION
#

from project import app

rparser = api.parser()
rparser.add_argument('login_id', type=str, required=True)
rparser.add_argument('password', type=str, required=True)

@nsp.route("/session")
class _auth(Resource):
    @api.expect(rparser)
    def post(self):
        if current_user.is_authenticated:
            resp = jsonify(error='Already logged in', mimetype='application/json')
            return make_response(resp, 400)
        else:
            args = rparser.parse_args(strict=True)
            user = User.query.filter_by(login_id=args['login_id']).first()
            if user and user.is_correct_password(args['password']):
                login_user(user, remember=True)
                s = JSONWebSignatureSerializer(app.config['SECRET_KEY'])
                token = s.dumps({'login_id': args['login_id'], 'password' : args['password']})
                resp = jsonify(message = "Logged in successfully", login_id=current_user.login_id, token=token.decode('utf-8'))
                return make_response(resp, 200)
            else:
                resp = jsonify(message = "Authentication error")
                return make_response(resp, 400)

    def delete(self):
        if current_user.is_authenticated:
            user = current_user.login_id
            logout_user()
            return make_response(jsonify(message="User " + user + " logged out"), 200)
        else:
            return make_response(jsonify(message="Not currently logged in"), 400)


@nsp.route("/token")
class _token(Resource):
    def get(self):
        pass

    def delete(self):
        pass
