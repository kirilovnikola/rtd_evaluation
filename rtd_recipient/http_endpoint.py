from flask import Flask
from flask import request
import json,sys
import calendar
import time
import csv

try:
    port_id = sys.argv[1]
except:
    print("Failed to assign arguments! Using default port 5001.")
    port_id = "5001"

app = Flask(__name__)
with open('receipt_'+port_id+'.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    #Create endpoint
    @app.route("/", methods=['GET', 'POST'])
    #Define function for the endpoint
    def index():
        #Check if request method is post
        if request.method == 'POST':
            #check if there is data
            if request.data:
                try:
                    #Try to serialize data
                    rtd_data = json.loads(request.data.decode(encoding='utf-8'))
                    #Print data or implement any other action here
                    print("Real-time data from reverse proxy: "+json.dumps(rtd_data))
                    time_stamp = int(time.time() * 1000)
                

                    writer.writerow([time_stamp])
                    return '200'
                except:
                    #if serialization fails
                    print("Error")
                    return '404'
        #No data or method is not "POST" return status code 404
        return '404'

    @app.route("/Observation/<id>", methods=['PUT'])
    #Define function for the endpoint
    def receive_sub(id):
        
        #check if there is data
        if request.data:
            try:
                #Try to serialize data
                rtd_data = json.loads(request.data.decode(encoding='utf-8'))
                #Print data or implement any other action here
                print("Real-time data Observation (ID:"+id+") from rest-hooks: "+json.dumps(rtd_data))
                
                time_stamp = int(time.time() * 1000)
                

                writer.writerow([time_stamp])
                return '200'
            except:
                #if serialization fails
                print("Error")
                return '404'



    if __name__ == "__main__":
        app.run(host='localhost', port=port_id)
