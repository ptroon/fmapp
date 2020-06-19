from flask import Flask, Blueprint, url_for, jsonify, make_response, request, Response
from flask_restplus import Api, Resource, reqparse
from flask_login import login_required, login_user, logout_user, current_user
from itsdangerous import JSONWebSignatureSerializer
import json

from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import literal
from sqlalchemy import not_, and_, or_

from project.models import *
from project import app, db, is_admin, mail, get_user
from project.gui.forms import *
from project.gui.logic import *


api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/fpa/api")
api = Api(api_blueprint, version = "1.0", \
      title = "Firewall Booking API",
      description = "Provide access to Firewall Bookings via an API")

nsp = api.namespace('v1', description='Firewall Booking Automation APIs v1')
nsp2 = api.namespace('v2', description='Firewall Booking Automation APIs v2')

# returns an error & code in JSON format
def json_error(_message, _code):
    message = json.dumps({'errors': _message})
    return Response(message, status=_code, mimetype='application/json')

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
@nsp.route("/user/<int:id>")
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


@nsp.route("/calendar")
class _doi(Resource):
    def get(self):

            a = aliased(DateOfInterest)
            b = aliased(Parameter)
            c = aliased(Booking)
            d = aliased(Complex)
            e = aliased(ComplexGroup)

            d1 = request.args.get("start", None)
            d2 = request.args.get("end", None)

            try:

                if (not d1 or not d2):
                    raise Exception ("start or end dates not provided on URL e.g. (?start=<date>&end=<date>)")

                d1 = datetime.strptime(d1.replace('+01:00','Z'), '%Y-%m-%dT%H:%M:%SZ')
                d2 = datetime.strptime(d2.replace('+01:00','Z'), '%Y-%m-%dT%H:%M:%SZ')

                #########################################################################
                # get queries from database
                # (start between d1 and d2) AND (end between d1 and d2) OR (start < d1 AND d2 < end)

                # get dates/events
                doi_ = db.session.query(a.id, a.doi_start_dt.label("start"), a.doi_end_dt.label("end"), \
                a.doi_name.label("title"), a.doi_comment.label("description"), \
                b.param_name.label("type"), b.param_value.label("style"),\
                b.id.label("typeid"), literal("DATE").label("eventType"), \
                func.fmapp.rem_slots(a.id).label("availableSlots"), e.max_slots.label("maxSlots")).\
                join(b, a.doi_type==b.id).\
                outerjoin(e, a.doi_filter==e.id).\
                filter(((a.doi_start_dt.between(d1, d2)) | \
                (a.doi_end_dt.between(d1, d2))) | \
                ((a.doi_start_dt < d1) & (d2 < a.doi_end_dt)))

                # get bookings
                bookings_ = db.session.query(c.id, c.start_dt.label("start"), c.end_dt.label("end"), \
                c.title.label("title"), c.owner_id.label("owner"), c.description.label("description"), \
                d.complex_name.label("complex"), c.approved_date.label("approved"),\
                literal("BOOKING").label("eventType")).\
                filter(c.complex == d.id).\
                filter(c.slot_id == 0.0).\
                filter(((c.start_dt.between(d1, d2)) | \
                (c.end_dt.between(d1, d2))) | \
                ((c.start_dt < d1) & (d2 < c.end_dt)))

                #########################################################################
                # subquery and then add columns and filter on events with types
                subq_events_ = doi_.subquery()
                events_ = db.session.query(subq_events_).all()

                subq_booking_approved_ = bookings_.subquery()
                booking_approved_ = db.session.query(subq_booking_approved_, literal("background-color: #DAFFB9; color: #000000;").label("style"), \
                literal("black").label("textColor")). \
                filter(subq_booking_approved_.c.approved.isnot(None)).all()

                subq_booking_notapproved_ = bookings_.subquery()
                booking_notapproved_ = db.session.query(subq_booking_notapproved_, literal("background-color: #CCCCCC; color: #000000;").label("style"), \
                literal("black").label("textColor")). \
                filter(subq_booking_notapproved_.c.approved.is_(None)).all()

                #########################################################################
                # turn into a list of dicts and extend for the extra queries
                result = list(map(lambda x: x._asdict(), events_))
                result.extend(list(map(lambda x: x._asdict(), booking_approved_)))
                result.extend(list(map(lambda x: x._asdict(), booking_notapproved_)))


            except Exception as ex:
                return json_error("error " + str(ex) + " getting calendar events", 400)

            return result

#################################################################
# COMPLEXES #
#############
@nsp.route("/complexes", defaults={'complex_type': '0'})
@nsp.route("/complexes/<int:complex_type>")
class _complexes(Resource):
    def get(self, complex_type):


            # get query from database
            a = aliased(Parameter)
            b = aliased(Parameter)
            c = aliased(Parameter)
            d = aliased(Parameter)

            if complex_type > 0: # return the specific list of complexes

                complexes_ = db.session.query(Complex.id, Complex.complex_name, Complex.complex_push_days, \
                Complex.complex_push_start, Complex.complex_push_end, a.param_value.label("complex_manager"), \
                b.param_value.label("vendor"), b.id.label("complex_type"), \
                c.param_value.label("complex_country"), d.param_name.label("complex_active")).\
                filter(b.id == complex_type). \
                join(a,Complex.complex_manager==a.id).join(b,Complex.complex_type==b.id).\
                join(c,Complex.complex_country==c.id).join(d,Complex.complex_active==d.id).all()

            else: # return all complexes as zero is the flag for everything

                complexes_ = db.session.query(Complex.id, Complex.complex_name, Complex.complex_push_days, \
                Complex.complex_push_start, Complex.complex_push_end, a.param_value.label("complex_manager"), \
                b.param_value.label("vendor"), b.id.label("complex_type"), \
                c.param_value.label("complex_country"), d.param_name.label("complex_active")).\
                join(a,Complex.complex_manager==a.id).join(b,Complex.complex_type==b.id).\
                join(c,Complex.complex_country==c.id).join(d,Complex.complex_active==d.id).all()

            result = list(map(lambda x: x._asdict(), complexes_))

            return result

#################################################################
# PARAMETERS #
@nsp.route("/parameters", defaults={'p_group': '0'})
@nsp.route("/parameters/<int:p_group>")
class _parameters(Resource):
    def get(self, p_group):
        if is_admin():

            parameters_ = db.session.query(Parameter.id, Parameter.param_name, Parameter.param_value).filter(Parameter.param_group == p_group).all()
            result = list(map(lambda x: x._asdict(), parameters_))
            return result

        else:
            return not_admin()


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
