import psycopg2
import json
import select
import csv,sys
import time

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
try:
    file_name = sys.argv[1]
except:
    file_name = "default_filename"
    print("Failed to assign filename!")
#Connect to db server
#Enter here the settings of your PostgreSQL
connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="fhir")
#Autocommit enabled - crucial for instant messages - LISTEN and NOTIFY
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

def db_listen():
    with open(file_name+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        cur = connection.cursor()
        cur.execute("LISTEN fhir_db_trigger_rtd;")
        while True:
            if select.select([connection], [], [], 5) != ([], [], []):
                #wait untill message
                connection.poll()                  
                #read message
                
                while connection.notifies:
                    #pop notification out of the list
                    notification =  connection.notifies.pop(0)  
                    #print message or implement any other activity
                    time_stamp = int(time.time() * 1000)
                

                    writer.writerow([time_stamp])
                    print(notification.payload)

                
db_listen()