from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
import redis
# from rq import Queue
import time
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
CORS(app)
db = SQLAlchemy(app)
# r = redis.Redis()
# q = Queue(connection=r)

from flaskblg import route
