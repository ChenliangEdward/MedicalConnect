from flaskblg import db
import os

os.remove("C:\\Users\\16178\\Desktop\\EC530\\MedicalConnect\\flaskblg\\site.db")
db.create_all()
