# from flask_restful import Resource, reqparse
# from flaskblg.models import *
# from flaskblg import api
#
# user_put_args = reqparse.RequestParser()
# user_put_args.add_argument("gender", type=str, help="the gender of the user", required=True)
# user_put_args.add_argument("full_name", type=str, help="the name of the user", required=True)
# user_put_args.add_argument("email", type=str, help="the email of the user", required=True)
# user_put_args.add_argument("role", type=str, help="the role of the user", required=True)
# users = {}
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
