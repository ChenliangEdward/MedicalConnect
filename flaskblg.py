from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
