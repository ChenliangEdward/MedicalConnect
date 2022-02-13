from flask import Flask
from flaskblg.models import *
from flaskblg import app


@app.route("/")
def hello_world():
    return "<h1>Welcome to MedicalConnect! </h1>"
