import requests

BASE = "http://127.0.0.1:5000/"

# testing User Put

# add User1 patient
response_patient = requests.put(BASE + "/api/users", {"gender": "male", "role": "patient", "email": "patient@bu.edu",
                                                      "full_name": "Chenliang Wang", "password": "patient"})
assert (response_patient.status_code == 201)

# add User2 doctor
response_doctor = requests.put(BASE + "/api/users", {"gender": "male", "role": "doctor", "email": "doctor@bu.edu",
                                                     "full_name": "Chenliang Wang", "password": "doctor"})
assert (response_doctor.status_code == 201)

# add User3 admin
response_admin = requests.put(BASE + "/api/users",
                              {"gender": "male", "role": "administrator", "email": "admin@bu.edu",
                               "full_name": "Chenliang Wang", "password": "administrator"})
assert (response_admin.status_code == 201)
#
#
# re-add User1
response_patient = requests.put(BASE + "/api/users", {"gender": "male", "role": "patient", "email": "patient@bu.edu",
                                                      "full_name": "Chenliang Wang", "password": "asdfasdf"})
assert (response_patient.status_code == 409)

# re-add type a false role
response_patient = requests.put(BASE + "/api/users", {"gender": "male", "role": "dumb", "email": "patient3@bu.edu",
                                                      "full_name": "Chenliang Wang", "password": "asdfasdf"})
assert (response_patient.status_code == 409)
