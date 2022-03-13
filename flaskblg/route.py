import flask
from flask import request
from flaskblg.models import *
from flaskblg import app
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

api = Api(app)

# TODO: def abort_if

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


class Users(Resource):
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        result = User.query.get(user_id)
        if not result:
            abort(404, message="No such user found...")
        return result

    @marshal_with(user_resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()

        # Check existing record
        result = User.query.get(user_id)
        if result:
            abort(409, message="User exists!")
        result = User.query.filter_by(args["email"]).first()
        if result:
            abort(409, message="email exists!")

        new_user = User(id=user_id, gender=args['gender'], full_name=args['full_name'], role=args['role'],
                        email=args['email'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        print(">>>>LOG<<<< : complete!")

        if args['role'] == 'patient':
            new_patient = Patients(patient_id=user_id)
            db.session.add(new_patient)
        if args['role'] == 'Administrator':
            new_admin = Admins(admin_id=user_id)
            db.session.add(new_admin)
        if args['role'] == 'doctor':
            new_doctor = MedicalProfessionals(mp_id=user_id)
            db.session.add(new_doctor)
        db.session.commit()
        return new_user, 201

    # TODO: Delete, Patch


admin_patch_args = reqparse.RequestParser()
admin_patch_args.add_argument("admin_id", type=int, help="the admin_id of the user")

admin_resource_fields = {"admin_id"}


class Administrator(Resource):
    @marshal_with(admin_resource_fields)
    def get(self, admin_id):
        result = Admins.query.get(admin_id)
        if not result:
            abort(404, message="No such admin found...")
        return result


mp_patch_args = reqparse.RequestParser()
mp_patch_args.add_argument("weight", type=float, help="the weight of the user")
mp_patch_args.add_argument("profession", type=str, help="the address of the user")

mp_resource_fields = {"mp_id",
                      "profession"}


class MedicalProfessionals(Resource):
    @marshal_with(mp_resource_fields)
    def get(self, mp_id):
        result = Admins.query.get(mp_id)
        if not result:
            abort(404, message="No such admin found...")
        return result

    @marshal_with(mp_resource_fields)
    def patch(self, mp_id):
        args = mp_patch_args.parse_args()
        result = MedicalProfessionals.query.filter_by(id=mp_id).first()
        if not result:
            abort(404, message='the Medical Professional does not exist')
        if "profession" in args:
            result.profession = args['profession']


patient_patch_args = reqparse.RequestParser()
patient_patch_args.add_argument("weight", type=float, help="the weight of the user")
patient_patch_args.add_argument("address", type=str, help="the address of the user")
patient_patch_args.add_argument("symptoms", type=str, help="the symptoms of the user")
patient_patch_args.add_argument("dob", type=str, help="the data of Birth of the user")

patient_resource_fields = {
    'patient_id': fields.Integer,
    'weight': fields.Float,
    'address': fields.String,
    'symptoms': fields.String,
    'dob': fields.String
}


class Patients(Resource):
    @marshal_with(patient_resource_fields)
    def get(self, patient_id):
        result = Patients.query.get(patient_id)
        if not result:
            abort(404, message="No such user found...")
        return result

    @marshal_with(patient_resource_fields)
    def patch(self, patient_id):
        args = patient_patch_args.parse_args()
        result = Patients.query.filter_by(id=patient_id).first()
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


device_put_args = reqparse.RequestParser()
device_put_args.add_argument("reading_id", help="the reading id of the device", required=True)
device_put_args.add_argument("usage", help="the usage of the device", required=True)
device_put_args.add_argument("serialNum", help="the serialNum of the device", required=True)
device_put_args.add_argument("assignedTo", help="what patient owns this device", required=True)
device_put_args.add_argument("assignedBy", help="who assigned this device", required=True)

device_resource_fields = {
    'reading_id': fields.Integer,
    'usage': fields.Float,
    'serialNum': fields.String,
    'assignedTo': fields.String,
    'assignedBy': fields.String
}


class Devices(Resource):
    @marshal_with(device_resource_fields)
    def get(self, reading_id):
        result = Devices.query.get(reading_id)
        if not result:
            abort(404, message="no such reading found")
        return result

    @marshal_with(device_resource_fields)
    def put(self, reading_id):
        args = device_put_args.parse_args()
        result = Devices.query.get(reading_id)
        if result:
            abort(409, message="Device exists!")
        new_device = Devices(reading_id=reading_id, usage=args['usage'], serialNum=args['serialNum'],
                             assignedTo=args['assignedTo'], assignedBy=args['assignedBy'])
        db.session.add(new_device)
        db.session.commit()
        print(">>>>LOG_Device<<<< : complete!")

    @marshal_with(device_resource_fields)
    def patch(self, reading_id):
        args = device_put_args.parse_args()
        result = Devices.query.filter_by(id=reading_id).first()
        if not result:
            abort(404, message='measure does not exist')
        if "usage" in args:
            result.weight = args['usage']
        if "serialNum" in args:
            result.address = args['serialNum']
        if "assignedTo" in args:
            result.symptoms = args['assignedTo']
        if "assignedBy" in args:
            result.dob = args['assignedBy']
        db.session.add(result)
        db.session.commit()


api.add_resource(Users, "/api/users/<int:user_id>")
api.add_resource(Patients, "/api/patients/<int:patient_id>")
api.add_resource(Devices, "/api/devices/<int:reading_id>")


@app.route("/")
def hello_world():
    return "<h1>Welcome to MedicalConnect! </h1>"


@app.route("/register", methods=['GET', 'POST'])
# TODO: change it to only deliver the page
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
