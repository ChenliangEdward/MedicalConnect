import requests

BASE = "http://127.0.0.1:5000/"

# testing User Get

#
#
email = "patient@bu.edu"
password_correct = "patient"
password_wrong = "wrongpassword"
response_get_patient = requests.get(BASE + "/api/users",
                                    {"email": email, "password": password_correct})
print(response_get_patient.json())
assert (response_get_patient.status_code == 201)
# testing wrong password
response_get_patient = requests.get(BASE + "/api/users",
                                    {"email": email, "password": password_wrong})
assert (response_get_patient.status_code == 404)

# testing null user
email = "null@bu.edu"
response_get_patient = requests.get(BASE + "/api/users",
                                    {"email": email, "password": password_correct})
assert (response_get_patient.status_code == 404)
