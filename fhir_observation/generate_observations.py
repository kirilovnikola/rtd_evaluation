import requests
import json
import sys
import calendar
import time
import csv

auth = 0 #Authentication needed (only basic auth supported)
fhir_user = "admin"
fhir_password = "password"
fhir_url= "http://localhost:8080/fhir/Observation/"

try:
    patient_id = sys.argv[1]
except:
    print("Failed to assign patient id!")
    sys.exit()

#prepare for post request to FHIR Server
session = requests.Session()
if(auth != 0):
    session.auth = (fhir_user,fhir_password)
    auth_req = session.post(fhir_url, verify=False)
    if auth_req.status_code != 200:
        print("Failed to authenticate!")
        sys.exit()
with open('generation_timestamps.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    for i in range(1000):
        f = open('observation.json')

        payload = json.load(f)
        payload["subject"]["reference"]= "Patient/"+patient_id

        time_stamp = int(time.time() * 1000)
        writer.writerow([time_stamp])
        r = session.post(fhir_url, json=payload, verify=False)
        if r.status_code != 201:
                print("Failed to post Subscription resource!")
                print(r.text)
                sys.exit()
        else:


            print("Current timestamp:", time_stamp)
        f.close()


    

