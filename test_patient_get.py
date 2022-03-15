import requests

BASE = "http://127.0.0.1:5000/"

email = "patient@bu.edu"
password_correct = "patient"

response = requests.get(BASE + "/api/patients", {"email": email, "password": password_correct})
print(response.json())
assert (response.status_code == 201)
