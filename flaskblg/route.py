import flask
from flask import request
from flaskblg.models import *
from flaskblg import app
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
import json
import time
from datetime import datetime
import requests
import random

# Start DB:
# from flaskblg import db
# db.create_all()
api = Api(app)


# TODO: def abort_if

def random_userid():
    r1 = random.randint(100000, 1000000000)
    return r1


# API implementation:
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("gender", type=str, help="the gender of the user", required=True)
user_put_args.add_argument("full_name", type=str, help="the name of the user", required=True)
user_put_args.add_argument("role", type=str, help="the role of the user", required=True)
user_put_args.add_argument("email", type=str, help="the email of the user", required=True)
user_put_args.add_argument("password", type=str, help="the password of the user", required=True)

user_resource_fields = {
    'id': fields.Integer,
    'full_name': fields.String,
    'gender': fields.String,
    'email': fields.String,
    'password': fields.String,
    'role': fields.String
}

user_get_args = reqparse.RequestParser()
user_get_args.add_argument("email", type=str, help="the email of the user", required=True)
user_get_args.add_argument("password", type=str, help="the password of the user", required=True)


class Users(Resource):
    # Get User information
    @marshal_with(user_resource_fields)
    def get(self):
        args = user_get_args.parse_args()
        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        return result

    # User Signup
    @marshal_with(user_resource_fields)
    def put(self):
        args = user_put_args.parse_args()

        # Check existing record
        result = User.query.filter_by(email=args["email"]).first()
        if result:
            abort(409, message="email exists!")

        user_id = random_userid()
        new_user = User(id=user_id, gender=args['gender'], full_name=args['full_name'], role=args['role'],
                        email=args['email'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        print(">>>>LOG<<<< : complete!")

        if args['role'] == 'patient':
            # print(args["email"])
            # new_patient = Patients(patient_id=user_id, email=args["email"])
            new_patient = Patients(patient_id=user_id)
            db.session.add(new_patient)
        if args['role'] == 'administrator':
            new_admin = Admins(admin_id=user_id, email=args["email"])
            db.session.add(new_admin)
        if args['role'] == 'doctor':
            new_doctor = MedicalProfessionals(mp_id=user_id, email=args["email"])
            db.session.add(new_doctor)
        db.session.commit()
        return new_user, 201

    # TODO: Delete, Patch


admin_get_args = reqparse.RequestParser()
admin_get_args.add_argument("email", type=str, help="the email of the admin", required=True)

admin_resource_fields = {'admin_id': fields.Integer,
                         'admin_email': fields.String}


class Administrator(Resource):
    @marshal_with(admin_resource_fields)
    def get(self):
        args = admin_get_args.parse_args()
        result = Admins.query.filter_by(args['email']).first()
        if not result:
            abort(404, message="No such admin found...")
        return result


mp_patch_args = reqparse.RequestParser()
mp_patch_args.add_argument("profession", type=str, help="the profession of the user")
mp_patch_args.add_argument("email", type=str, help="the email of the user", required=True)
mp_patch_args.add_argument("password", type=str, help="the password of the MP", required=True)
mp_patch_args.add_argument("mp_available", type=str, help="the available time of the MP")

mp_resource_fields = {"mp_id": fields.Integer,
                      "mp_email": fields.String,
                      "mp_available": fields.String,
                      "mp_profession": fields.String}


class MedicalProfessionalsAPI(Resource):
    @marshal_with(mp_resource_fields)
    def get(self):
        args = mp_patch_args.parse_args()

        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = MedicalProfessionals.query.filter_by(args["email"]).first()
        if not result:
            abort(404, message="No such admin found...")
        return result

    @marshal_with(mp_resource_fields)
    def patch(self):
        args = mp_patch_args.parse_args()

        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = MedicalProfessionals.query.filter_by(email=args["email"]).first()
        if not result:
            abort(404, message='the Medical Professional does not exist')
        if "profession" in args:
            result.profession = args['profession']
        if "mp_available" in args:
            result.mp_available = args['mp_available']
        db.session.add(result)
        db.session.commit()


patient_patch_args = reqparse.RequestParser()
patient_patch_args.add_argument("weight", type=float, help="the weight of the user")
patient_patch_args.add_argument("address", type=str, help="the address of the user")
patient_patch_args.add_argument("symptoms", type=str, help="the symptoms of the user")
patient_patch_args.add_argument("dob", type=str, help="the data of Birth of the user")
patient_patch_args.add_argument("password", type=str, help="the data of Birth of the user", required=True)
patient_patch_args.add_argument("email", type=str, help="the data of Birth of the user", required=True)

patient_resource_fields = {
    'patient_id': fields.Integer,
    'weight': fields.Float,
    'address': fields.String,
    'symptoms': fields.String,
    'dob': fields.String
}


class PatientsAPI(Resource):
    @marshal_with(patient_resource_fields)
    def get(self):
        args = patient_patch_args.parse_args()
        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = Patients.query.filter_by(email=args["email"]).first()
        if not result:
            abort(404, message="No such user found...")
        return result

    @marshal_with(patient_resource_fields)
    def patch(self):
        args = patient_patch_args.parse_args()

        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = Patients.query.filter_by(email=args["email"]).first()
        if not result:
            abort(404, message='patient does not exist')
        if "weight" in args:
            result.weight = args['weight']
        if "address" in args:
            result.address = args['address']
        if "symptoms" in args:
            result.symptoms = args['symptoms']
        if "dob" in args:
            result.dob = args['dob']
        db.session.add(result)
        db.session.commit()

        return result


appointment_put_args = reqparse.RequestParser()
appointment_put_args.add_argument("patient_email", type=float, help="the email of the patient", required=True)
appointment_put_args.add_argument("mp_email", type=str, help="the email of the mp", required=True)
appointment_put_args.add_argument("timeStart", type=str, help="the start time of the appointment", required=True)
appointment_put_args.add_argument("timeEnd", type=str, help="the end time of the appointment", required=True)
appointment_put_args.add_argument("message", type=str, help="the message of the appointment")
appointment_put_args.add_argument("email", type=str, help="the email of the request user", required=True)
appointment_put_args.add_argument("password", type=str, help="the password the user", required=True)

appointment_get_args = reqparse.RequestParser()
appointment_get_args.add_argument("email", type=str, help="the email of the request user", required=True)
appointment_get_args.add_argument("password", type=str, help="the password the user", required=True)

appointment_resource_fields = {
    'appointment_id': fields.Integer,
    'patient_email': fields.String,
    'mp_email': fields.String,
    'timeStart': fields.Integer,
    'timeEnd': fields.Integer,
    'message': fields.String
}


class AppointmentsAPI(Resource):
    @marshal_with(appointment_resource_fields)
    def get(self):
        args = appointment_get_args.parse_args()
        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        # get appointments
        if result.role == "patient":
            result = Appointments.query.filter_by(patient_email=args['email']).all()
        elif result.role == "doctor":
            result = Appointments.query.filter_by(mp_email=args['email']).all()
        if not result:
            abort(404, message="no appointments yet")
        return result

    @marshal_with(appointment_resource_fields)
    def put(self):
        args = appointment_put_args.parse_args()
        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        # put to DB
        appointment_id = random_userid()
        new_appointment = Appointments(reading_id=appointment_id, patient_email=args['patient_email'],
                                       mp_email=args['mp_email'],
                                       timeStart=args['timeStart'], timeEnd=args['timeEnd'], message=args['message'])
        db.session.add(new_appointment)
        db.session.commit()
        print(">>>>LOG_Appointment<<<< : complete!")


device_put_args = reqparse.RequestParser()
device_put_args.add_argument("reading_id", help="the reading id of the device", required=True)
device_put_args.add_argument("usage", type=str, help="the usage of the device", required=True)
device_put_args.add_argument("serialNum", type=str, help="the serialNum of the device", required=True)
device_put_args.add_argument("assignedTo", type=str, help="what patient owns this device", required=True)
device_put_args.add_argument("assignedBy", type=str, help="who assigned this device", required=True)

device_put_args.add_argument("password", type=str, help="the password of the user", required=True)
device_put_args.add_argument("email", type=str, help="who sent this request", required=True)

device_get_args = reqparse.RequestParser()
device_get_args.add_argument("password", type=str, help="the password of the user", required=True)
device_get_args.add_argument("email", type=str, help="who sent this request", required=True)
device_get_args.add_argument("role", type=str, help="who checked this email", required=True)

device_resource_fields = {
    'reading_id': fields.Integer,
    'usage': fields.Float,
    'serialNum': fields.String,
    'assignedTo': fields.String,
    'assignedBy': fields.String,
    'add_date': fields.Integer
}


class DevicesAPI(Resource):
    @marshal_with(device_resource_fields)
    def get(self):
        args = device_get_args.parse_args()

        # Password Authentication
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        # if it is the Patient:
        if args['role'] == "patient":
            result = Devices.query.filter_by(assignedTo=args['email']).all()
        elif args['role'] == "mp":
            result = Devices.query.filter_by(assignedBy=args['email']).all()
        if not result:
            abort(404, message="no such reading found")
        return result

    @marshal_with(device_resource_fields)
    def put(self):
        args = device_put_args.parse_args()

        # Password Authentication
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        reading_id = random_userid()
        new_device = Devices(reading_id=reading_id, usage=args['usage'], serialNum=args['serialNum'],
                             assignedTo=args['assignedTo'], assignedBy=args['assignedBy'], add_date=int(time.time()))
        db.session.add(new_device)
        db.session.commit()
        print(">>>>LOG_Device<<<< : complete!")

    # @marshal_with(device_resource_fields)
    # def patch(self):
    #     args = device_put_args.parse_args()
    #     result = Devices.query.filter_by(id=reading_id).first()
    #     if not result:
    #         abort(404, message='measure does not exist')
    #     if "usage" in args:
    #         result.weight = args['usage']
    #     if "serialNum" in args:
    #         result.address = args['serialNum']
    #     if "assignedTo" in args:
    #         result.symptoms = args['assignedTo']
    #     if "assignedBy" in args:
    #         result.dob = args['assignedBy']
    #     db.session.add(result)
    #     db.session.commit()


message_args = reqparse.RequestParser()
message_args.add_argument("from", help="who sends this", required=True)
message_args.add_argument("to", help="who receive this, email", required=True)
message_args.add_argument("Message", help="the body of the message", required=True)
# message_args.add_argument("Datetime", help="what time is itd", required=True)
message_args.add_argument("password", help="the password of the sender", required=True)

message_resource_fields = {
    'from': fields.Integer,
    'to': fields.Float,
    'Message': fields.String,
    'password': fields.String
}


def insert_message(f, t, m):
    timestamp = int(time.time())
    # dt = datetime.fromtimestamp(timestamp)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'CU8wXM1sLJLA40qxvvhVr4IaldsJY7xtZBnnJN0d6zV9cSuStUmGLSXvSGnbozSO',
    }
    json_data = {
        'dataSource': 'Cluster0',
        'database': 'test',
        'collection': 'test',
        'document': {
            'from': f,
            'to': t,
            'Message': m,
            'Datetime': str(timestamp)
        },
    }
    response = requests.post(
        'https://data.mongodb-api.com/app/data-nfawj/endpoint/data/beta/action/insertOne', headers=headers,
        json=json_data)


def find_message(f, t):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'CU8wXM1sLJLA40qxvvhVr4IaldsJY7xtZBnnJN0d6zV9cSuStUmGLSXvSGnbozSO',
    }

    json_data = {
        'dataSource': 'Cluster0',
        'database': 'test',
        'collection': 'test',
        'filter': {
            'from': f,
            'to': t
        },
    }
    response = requests.post(
        'https://data.mongodb-api.com/app/data-nfawj/endpoint/data/beta/action/find',
        headers=headers,
        json=json_data)
    my_json = response.content.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    # print(s)
    return data


def get_conversation(f, t):
    ft = find_message(f, t)
    tf = find_message(t, f)
    l1 = ft['documents']
    l2 = tf['documents']
    l = l1 + l2
    for i in l:
        i['Datetime'] = int(i['Datetime'])
    l = sorted(l, key=lambda x: x['Datetime'], reverse=False)
    return l


class Messages(Resource):
    @marshal_with(message_resource_fields)
    def put(self):
        args = message_args.parse_args()

        # authentication
        result = User.query.filter_by(args['from'])
        if not result:
            abort(404, message='user email does not exist')
        result = User.query.filter_by(args['to'])
        if not result:
            abort(404, message='receiver email does not exist')

        # Check if the password matches
        password_check = User.query.filter_by(args['from']).first()
        if args['password'] != password_check['password']:
            abort(404, message='user password does not match')
        try:
            insert_message(args['from'], args['to'], args['Message'])
        except:
            abort(404, message='cannot send message')

        return {"Message sent"}

    @marshal_with(message_resource_fields)
    def get(self):
        args = message_args.parse_args()
        result = User.query.filter_by(args['from'])
        if not result:
            abort(404, message='user email does not exist')
        result = User.query.filter_by(args['to'])
        if not result:
            abort(404, message='receiver email does not exist')
        # Check if the password matches
        password_check = User.query.filter_by(args['from']).first()
        if args['password'] != password_check['password']:
            abort(404, message='user password does not match')
        message_retrieved = get_conversation(args['from'], args['to'])
        return json.dumps(message_retrieved)


api.add_resource(Users, "/api/users")
api.add_resource(PatientsAPI, "/api/patients")
api.add_resource(DevicesAPI, "/api/devices")
api.add_resource(Messages, "/api/messages")
api.add_resource(AppointmentsAPI, "/api/appointments")


# api.add_resource(AppointmentsAPI, "/api/appointments")


@app.route("/")
def hello_world():
    return "<h1>Welcome to MedicalConnect! </h1>"


@app.route("/register", methods=['GET', 'POST'])
def register():
    a = User.query.get(id=123)
    if request.method == 'POST':
        json_data = flask.request.json
        id = 1
        gender = json_data["gender"]
        full_name = json_data['full_name']
        role = json_data['role']
        email = json_data['email']
        password = json_data['password']

        return "Done"
    else:
        # id = 1
        # gender = request.args.get('gender')
        # full_name = request.args.get('full_name')
        # role = request.args.get('role')
        # email = request.args.get('email')
        # password = request.args.get('password')
        return "<h1>Register Page WIP</h1>"
