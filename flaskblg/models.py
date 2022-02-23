from datetime import datetime
from flaskblg import db


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    gender = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.full_name}','{self.email}')"


class Patients(db.Model):
    patient_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    weight = db.Column(db.Float)
    address = db.Column(db.String)
    symptoms = db.Column(db.String)
    dob = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Patients('{self.patient_id}')"


class MedicalProfessionals(db.Model):
    mp_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    profession = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"MedicalProfessionals('{self.mp_id}')"


class Admins(db.Model):
    admin_id = db.Column(db.Integer, nullable=False, primary_key=True)

    def __repr__(self):
        return f"Admins('{self.admin_id}')"


class Appointments(db.Model):
    appointment_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    patientID = db.Column(db.Integer, nullable=False)
    mpID = db.Column(db.Integer, unique=True, nullable=False)
    timeStart = db.Column(db.DateTime, nullable=False)
    timeEnd = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Appointments('{self.appointment_id}')"


class Devices(db.Model):
    reading_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    usage = db.Column(db.String(30), nullable=False)
    serialNum = db.Column(db.String(200), nullable=False)
    assignedTo = db.Column(db.Integer, nullable=False)
    assignedBy = db.Column(db.Integer, nullable=True)
