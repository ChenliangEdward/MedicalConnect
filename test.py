import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.put(BASE + "/api/users/0", {"gender": "male", "role": "Administrator", "email": "edwangd@bu.edu",
#                                     "full_name": "Chenliang Wang", "password": "8609EdWa!?,"})
# response = requests.get(BASE + "/api/users/1")
response = requests.put(BASE + "/api/users/2", {"gender": "male", "role": "doctor", "email": "edwangd2@bu.edu",
                                                "full_name": "Chenliang Wang", "password": "8609EdWa!?,"})
print(response.json())
