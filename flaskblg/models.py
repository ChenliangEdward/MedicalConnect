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
    dob = db.Column(db.String(30))
    patient_email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"Patients('{self.patient_id}')"


class MedicalProfessionals(db.Model):
    mp_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    mp_email = db.Column(db.String, unique=True, nullable=False)
    mp_available = db.Column(db.String)
    profession = db.Column(db.String(30))

    def __repr__(self):
        return f"MedicalProfessionals('{self.profession}')"


class Admins(db.Model):
    admin_id = db.Column(db.Integer, nullable=False, primary_key=True)
    admin_email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"Admins('{self.admin_id}')"


class Appointments(db.Model):
    appointment_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    patient_email = db.Column(db.String, nullable=False)
    mp_email = db.Column(db.String, unique=True, nullable=False)
    timeStart = db.Column(db.Integer, nullable=False)
    timeEnd = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Appointments('{self.appointment_id}')"


class Measures(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    related_device = db.Column(db.Integer, nullable=False)
    measurement = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)


class Devices(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    device_name = db.Column(db.String)
    model = db.Column(db.String)
    serial_num = db.Column(db.String, nullable=False)
    measure_type = db.Column(db.String, unique=True)
    assignedTo = db.Column(db.String, nullable=False)
    assignedBy = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Devices('{self.id}')"
