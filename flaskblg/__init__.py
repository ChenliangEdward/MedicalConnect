from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# api = Api(app)
#
# user_put_args = reqparse.RequestParser()
# user_put_args.add_argument("gender", type=str, help="the gender of the user", required=True)
# user_put_args.add_argument("full_name", type=str, help="the name of the user", required=True)
# user_put_args.add_argument("email", type=str, help="the email of the user", required=True)
# user_put_args.add_argument("role", type=str, help="the role of the user", required=True)
#
#
# # TODO: def abort_if
#
#
# # API implementation:
# class Users(Resource):
#     def get(self, userID):
#         result = db.User.query.get(id=userID)
#         return result
#
#     def put(self, user_id):
#         args = user_put_args.parse_args()
#         # TODO: add random number generator to create user
#         return {user_id: args}, 201
#
#     # TODO: Delete
#
#
# api.add_resource(Users, "/api/users/<int:user_id>")

from flaskblg import route
