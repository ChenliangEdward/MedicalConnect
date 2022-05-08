import flask
from flask import request
from flaskblg.models import *
# from flaskblg import app, r, q
from flaskblg import app
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
import json
import time
from datetime import datetime
# from s2t import real_time_transcription
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

        return result, 201

    # User Signup
    @marshal_with(user_resource_fields)
    def put(self):
        args = user_put_args.parse_args()

        # Check existing record
        result = User.query.filter_by(email=args["email"]).first()
        if result:
            abort(409, message="email exists!")

        user_id = random_userid()
        if args['role'] == 'patient':
            new_patient = Patients(patient_id=user_id, patient_email=args["email"])
            db.session.add(new_patient)
        elif args['role'] == 'administrator':
            new_admin = Admins(admin_id=user_id, admin_email=args["email"])
            db.session.add(new_admin)
        elif args['role'] == 'doctor':
            new_doctor = MedicalProfessionals(mp_id=user_id, mp_email=args["email"])
            db.session.add(new_doctor)
        else:
            abort(409, message="role not correctly specified")
        new_user = User(id=user_id, gender=args['gender'], full_name=args['full_name'], role=args['role'],
                        email=args['email'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        print(">>>>LOG<<<< : complete!")
        return new_user, 201


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
        return result, 201


mp_patch_args = reqparse.RequestParser()
mp_patch_args.add_argument("profession", type=str, help="the profession of the user")
mp_patch_args.add_argument("email", type=str, help="the email of the user", required=True)
mp_patch_args.add_argument("password", type=str, help="the password of the MP", required=True)
mp_patch_args.add_argument("mp_available", type=str, help="the available time of the MP")

mp_resource_fields = {"mp_id": fields.Integer,
                      "mp_email": fields.String,
                      "mp_available": fields.String,
                      "profession": fields.String}


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

        result = MedicalProfessionals.query.filter_by(mp_email=args["email"]).first()
        if not result:
            abort(404, message="No such admin found...")
        return result, 201

    @marshal_with(mp_resource_fields)
    def patch(self):
        args = mp_patch_args.parse_args()

        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = MedicalProfessionals.query.filter_by(mp_email=args["email"]).first()
        if not result:
            abort(404, message='the Medical Professional does not exist')
        if "profession" in args:
            result.profession = args['profession']
        if "mp_available" in args:
            result.mp_available = args['mp_available']
        print(result)
        db.session.add(result)
        db.session.commit()
        return result, 201


patient_patch_args = reqparse.RequestParser()
patient_patch_args.add_argument("weight", type=float, help="the weight of the user")
patient_patch_args.add_argument("address", type=str, help="the address of the user")
patient_patch_args.add_argument("symptoms", type=str, help="the symptoms of the user")
patient_patch_args.add_argument("dob", type=str, help="the data of Birth of the user")
patient_patch_args.add_argument("password", type=str, help="the user password", required=True)
patient_patch_args.add_argument("email", type=str, help="the email address of the user", required=True)

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

        result = Patients.query.filter_by(patient_email=args["email"]).first()
        if not result:
            abort(404, message="No such user found...")
        return result, 201

    @marshal_with(patient_resource_fields)
    def patch(self):
        args = patient_patch_args.parse_args()

        # password authenticate
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = Patients.query.filter_by(patient_email=args["email"]).first()
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
        return result, 201


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
device_put_args.add_argument("id", help="the reading id of the device")
device_put_args.add_argument("device_name", type=str, help="who assigned this device", required=True)
device_put_args.add_argument("model", type=str, help="the model of the device", required=True)
device_put_args.add_argument("measure_type", type=str, help="the measure_type of the device", required=True)
device_put_args.add_argument("serial_num", type=str, help="the serialNum of the device", required=True)
device_put_args.add_argument("assignedTo", type=str, help="what patient owns this device", required=True)
device_put_args.add_argument("assignedBy", type=str, help="who assigned this device", required=True)

device_put_args.add_argument("password", type=str, help="the password of the user", required=True)
device_put_args.add_argument("email", type=str, help="who sent this request", required=True)

device_get_args = reqparse.RequestParser()
device_get_args.add_argument("password", type=str, help="the password of the user", required=True)
device_get_args.add_argument("email", type=str, help="who sent this request", required=True)

device_get_args.add_argument("role", type=str, help="who checked this email", required=True)

device_delete_args = reqparse.RequestParser()
device_delete_args.add_argument("password", type=str, help="the password of the user", required=True)
device_delete_args.add_argument("email", type=str, help="who sent this request", required=True)
device_delete_args.add_argument("id", type=int, help="who sent this request", required=True)

device_resource_fields = {
    'id': fields.Integer,
    'device_name': fields.String,
    'usage': fields.Float,
    'serial_num': fields.String,
    'measure_type': fields.String,
    'assignedTo': fields.String,
    'assignedBy': fields.String,

    'email': fields.String,
    'password': fields.String,
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

        new_device = Devices(device_name=args['device_name'], model=args['usage'], serial_num=args['serial_num'],
                             measure_type=args['measure_type'],
                             assignedTo=args['assignedTo'], assignedBy=args['assignedBy'], timestamp=int(time.time()))
        db.session.add(new_device)
        db.session.commit()
        print(">>>>LOG_Device<<<< : complete!")
        return "Device Adding Complete!"

    @marshal_with(device_resource_fields)
    def delete(self):
        args = device_delete_args.parse_args()

        # Password Authentication
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        Devices.query.filter_by(id=args['id']).delete()
        db.session.commit()
        print("Delete Complete!")
        return "Device delete Complete!"


measure_put_args = reqparse.RequestParser()
measure_put_args.add_argument("related_device", type=str, help="", required=True)
measure_put_args.add_argument("measurement", type=str, help="")
measure_put_args.add_argument("unit", type=str, help="")
measure_put_args.add_argument("email", type=str, help="the email of the user", required=True)
measure_put_args.add_argument("password", type=str, help="the password of the MP", required=True)

measure_get_args = reqparse.RequestParser()
measure_get_args.add_argument("related_device", type=str, help="", required=True)
measure_get_args.add_argument("email", type=str, help="the email of the user", required=True)
measure_get_args.add_argument("password", type=str, help="the password of the MP", required=True)

measure_delete_args = reqparse.RequestParser()
measure_delete_args.add_argument("id", type=str, help="", required=True)
measure_delete_args.add_argument("email", type=str, help="the email of the user", required=True)
measure_delete_args.add_argument("password", type=str, help="the password of the MP", required=True)

measure_resource_fields = {
    'id': fields.String,
    'related_device': fields.String,
    'measurement': fields.String,
    'unit': fields.String,
    'email': fields.String,
    'password': fields.String,
}


class MeasurementsAPI(Resource):
    @marshal_with(measure_resource_fields)
    def get(self):
        args = measure_get_args.parse_args()
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        result = Measures.query.filter_by(related_device=args['related_device']).all()
        if not result:
            return "No Device Found!"
        else:
            return result

    @marshal_with(measure_resource_fields)
    def put(self):
        args = measure_put_args.parse_args()
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')
        new_measure = Measures(related_device=args['related_device'], measurement=args['measurement'],
                               unit=args['unit'],
                               timestamp=int(time.time()))
        db.session.add(new_measure)
        db.session.commit()

    @marshal_with(measure_delete_args)
    def delete(self):
        args = measure_get_args.parse_args()
        result = User.query.filter_by(email=args['email']).first()
        if not result:
            abort(404, message="No such user found...")
        if args["password"] != result.password:
            abort(404, message='user password does not match')

        Measures.query.filter_by(id=args['id']).delete()
        db.session.commit()
        print("Measures Complete!")
        return "Measures delete Complete!"


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
        result = User.query.filter_by(args['from']).first()
        if not result:
            abort(404, message='user email does not exist')
        result = User.query.filter_by(args['to']).first()
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


# class Voice(Resource):

api.add_resource(Users, "/api/users")
api.add_resource(PatientsAPI, "/api/patients")
api.add_resource(MedicalProfessionalsAPI, "/api/mps")
api.add_resource(Messages, "/api/messages")
api.add_resource(AppointmentsAPI, "/api/appointments")
# enter Measurements
api.add_resource(MeasurementsAPI, "/api/measurement")
# register device
api.add_resource(DevicesAPI, "/api/devices")


# api.add_resource(Voice, "/api/Voice")


# api.add_resource(AppointmentsAPI, "/api/appointments")


@app.route("/")
def hello_world():
    return "<h1>Welcome to MedicalConnect!</h1>\n<h2>The server is up and running, please test it with the user " \
           "document</h2> "


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
