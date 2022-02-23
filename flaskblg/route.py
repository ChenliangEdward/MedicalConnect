import flask
from flask import request
from flaskblg.models import *
from flaskblg import app
from flask_restful import Api, Resource, reqparse

api = Api(app)

# TODO: def abort_if


# API implementation:
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("gender", type=str, help="the gender of the user", required=True)
user_put_args.add_argument("full_name", type=str, help="the name of the user", required=True)
user_put_args.add_argument("role", type=str, help="the role of the user", required=True)
user_put_args.add_argument("email", type=str, help="the email of the user", required=True)
user_put_args.add_argument("password", type=str, help="the password of the user", required=True)


class Users(Resource):
    def get(self, user_id):
        result = str(User.query.filter_by(full_name="ChenliangWang"))
        return result

    def put(self, user_id):
        args = user_put_args.parse_args()
        new_user = User(id=user_id, gender=args['gender'], full_name=args['full_name'], role=args['role'],
                        email=args['email'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        print(">>>>LOG<<<< : complete!")
        return {user_id: args}, 201

    # TODO: Delete


api.add_resource(Users, "/api/users/<int:user_id>")


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
