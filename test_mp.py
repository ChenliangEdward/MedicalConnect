import requests

BASE = "http://127.0.0.1:5000/"
# BASE = "http://13.59.40.217/"

email = "doctor@bu.edu"
password_correct = "doctor"
password_wrong = "wrongpassword"
# test mp get

# success
response = requests.get(BASE + "/api/mps", {"email": email, "password": password_correct})
print(response.json())
assert (response.status_code == 201)

# fail
response = requests.get(BASE + "/api/mps", {"email": email, "password": password_wrong})
print(response.json())
assert (response.status_code == 404)

# test mp fetch
response1 = requests.patch(BASE + "/api/mps", {"email": email, "password": password_correct, "profession": "Dentist"})
print(response1.json())
assert (response1.status_code == 201)
