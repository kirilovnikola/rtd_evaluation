import requests
import json
import sys

auth = 0 #Authentication needed (only basic auth supported)
fhir_user = "admin"
fhir_password = "password"
fhir_url= "http://localhost:5000/fhir/Subscription/"
endpoint = "http://localhost:5001/" #For rest-hooks, we will use the target_server

try:
    patient_id = sys.argv[1]
    if sys.argv[2] == "websocket" or sys.argv[2] == "rest-hook":
        sub_channel_type = sys.argv[2]
        print(patient_id+" "+sub_channel_type)
    else:
        print("Wrong channel type!")
        sys.exit()
except:
    print("Failed to assign arguments!")

#prepare for post request to FHIR Server
session = requests.Session()
if(auth != 0):
    session.auth = (fhir_user,fhir_password)
    auth_req = session.post(fhir_url, verify=False)
    if auth_req.status_code != 200:
        print("Failed to authenticate!")
        sys.exit()
f = open('subscription.json')

payload = json.load(f)
payload["criteria"] = "Observation?subject="+patient_id+"&status=final"
payload["channel"]["type"] = sub_channel_type
payload["channel"]["endpoint"] = endpoint
r = session.post(fhir_url, json=payload, verify=False)
if r.status_code != 201:
        print("Failed to post Subscription resource!")
        print(r.text)
        sys.exit()
print(r.text)