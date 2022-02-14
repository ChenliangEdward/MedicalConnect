import flask
from flask import request
from flaskblg.models import *
from flaskblg import app


@app.route("/")
def hello_world():
    return "<h1>Welcome to MedicalConnect! </h1>"


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        json_data = flask.request.json
        id = 1
        gender = json_data["gender"]
        full_name = json_data['full_name']
        role = json_data['role']
        email = json_data['email']
        password = json_data['password']
        
        return "Done"
    # id = 1
    # gender = request.args.get('gender')
    # full_name = request.args.get('full_name')
    # role = request.args.get('role')
    # email = request.args.get('email')
    # password = request.args.get('password')

    return "<h1>Register Page WIP</h1>"
