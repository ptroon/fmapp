from flask import Flask, Blueprint, url_for, jsonify, make_response
from flask_restplus import Api, Resource, reqparse
from flask_login import login_required, login_user, logout_user, current_user
from itsdangerous import JSONWebSignatureSerializer
import json
from sqlalchemy.orm import aliased

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

# returns an error & code in JSON format
def json_error(_message, _code):
    return jsonify(error=_message, code=_code, mimetype="application/json")

def not_admin():
    return json_error("you are not an administrator or not logged in", 401)


#
# ENDPOINTS
#
@login_required
@nsp.route("/users")
class _users(Resource):
    def get(self):
        if is_admin():
            # get query from database
            users_ = db.session.query(User.id,User.forename,User.surname,User.comment,User.email,Role.role_name,Parameter.param_value)\
            .join(Role).outerjoin(Parameter).order_by(User.id.asc()).all()

            # create list of a map for query
            result = list(map(lambda x: x._asdict(), users_))
            #result = json.dumps(result, indent=4, sort_keys=True, default=json_fmt_default)
            return result

@login_required
@nsp.route("/user/<id>")
class _user(Resource):
    def get(self, id):
        if is_admin():
            # get query from database
            users_ = db.session.query(User.id, User.login_id, User.forename, User.surname, User.comment,\
                    User.email, Role.role_name, Parameter.param_value, User.enabled, User.created_date,
                    User.last_login, User.last_modified, User.modified_by)\
                    .join(Role).outerjoin(Parameter).filter(User.id==id).all()

            # create list of a map for query
            result = list(map(lambda x: x._asdict(), users_))
            #result = json.dumps(users_, indent=4, sort_keys=True, default=json_fmt_default)
            return result

        else:
            return not_admin()

#################################################################
# ROLES #
#########
@nsp.route("/roles")
class _roles(Resource):
    def get(self):
        if is_admin():
            # get query from database
            roles_ = db.session.query(Role.id, Role.role_name, Role.role_admin, Role.created_date, Role.enabled).all()

            # create list of a map for query
            result = list(map(lambda x: x._asdict(), roles_))
            return result

        else:
            return not_admin()

#################################################################
# DATES #
#########
@nsp.route("/dates")
class _dates(Resource):
    def get(self):
        if is_admin():
            # get query from database
            doi_ = db.session.query(DateOfInterest).all()

            result = []
            for subl in doi_:
                d = model_as_dict(subl)
                result.append(d)

            return result

        else:
            return not_admin()

#################################################################
# COMPLEXES #
#############
@nsp.route("/complexes")
class _complexes(Resource):
    def get(self):
        if is_admin():

            # get query from database
            a = aliased(Parameter)
            b = aliased(Parameter)
            c = aliased(Parameter)
            d = aliased(Parameter)

            complexes_ = db.session.query(Complex.id, Complex.complex_name, Complex.complex_push_days, \
            Complex.complex_push_start, Complex.complex_push_end, a.param_value.label("complex_manager"), \
            b.param_value.label("complex_type"), \
            c.param_value.label("complex_country"), d.param_name.label("complex_active")).\
            join(a,Complex.complex_manager==a.id).join(b,Complex.complex_type==b.id).\
            join(c,Complex.complex_country==c.id).join(d,Complex.complex_active==d.id).all()

            result = list(map(lambda x: x._asdict(), complexes_))

            return result

        else:
            return not_admin()

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

'''
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
'''
'''
@nsp.route("/token")
class _token(Resource):
    def get(self):
        pass

    def delete(self):
        pass
'''
