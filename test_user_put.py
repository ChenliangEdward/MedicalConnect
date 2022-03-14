import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "/api/users", {"gender": "male", "role": "patient", "email": "edwangd@bu.edu",
                                              "full_name": "Chenliang Wang", "password": "8609EdWa!?,"})

# response = requests.put(BASE + "/api/users", {"gender": "male", "role": "doctor", "email": "doctor@bu.edu",
#                                               "full_name": "Chenliang Wang", "password": "11111"})
