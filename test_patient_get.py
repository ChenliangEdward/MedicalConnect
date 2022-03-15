import requests

# BASE = "http://127.0.0.1:5000/"
BASE = "http://13.59.40.217/"

email = "patient@bu.edu"
password_correct = "patient"
password_wrong = "wrongpassword"
# test patient get

# success
response = requests.get(BASE + "/api/patients", {"email": email, "password": password_correct})
print(response.json())
assert (response.status_code == 201)

# fail
response = requests.get(BASE + "/api/patients", {"email": email, "password": password_wrong})
print(response.json())
assert (response.status_code == 404)

# test patch
dob = "1960/4/16"
response = requests.patch(BASE + "/api/patients", {"email": email, "password": password_correct, "dob": dob})
print(response.json())
assert (response.status_code == 201)
