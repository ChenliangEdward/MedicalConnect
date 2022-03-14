import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/api/patients", {"email": "edwangd@bu.edu", "password": "8609EdWa!?,"})
print(response.json())
