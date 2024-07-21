
# Evaluation of technical approaches for real-time data transfer from electronic health record systems
Author: Nikola Kirilov

In this repository you will find  reference implementations to evaluate the technical approaches for real-time data transfer from electronic health record systems

Warning: The provided code is not intended for production use. 

### REST Servers - HL7FHIR

### Usage
To use rest-hooks and websocket make sure to activate them. For HAPI FHIR the following lines in the "application.yaml" have to be uncommented and set to true:

```
subscription:
	resthook_enabled: true
	websocket_enabled: true
```

#### Creation of a Subscription resource

To use the script you need to install the requests library:

``` pip install requests```

By default the script does not use any authentication for the connection. If your server needs authentication we provide HTTP Basic Auth support. To use it you need to change line 5-7 of the script:

```python
auth = 1 #Authentication needed (only basic auth supported)
fhir_user = "user"
fhir_password = "password"
```
The url of the FHIR server and the endpoint for rest hooks is given in the variables line 8-9

```python
fhir_url= "http://localhost:5000/fhir/Subscription/"
endpoint = "http://localhost:5001/" #For rest-hooks, we will use the rtd recipient http endpoint
```
For endpoint you can use the http endpoint in "rtd_recipient".

The script is executed from terminal with the following two arguments:
[PID] - Id of the Patient resource for which we will generate notifications when an Observation resource is created
[CHANNEL] - channel type of the subscription (websocket or rest-hook)

```py subscriby.py [PID] [CHANNEL]```

After executing the script the Subscription resource is printed as a response in the terminal. It is important to note the Subscription resource id if you will use websockets.
#### RTD Recipient - HTTP-Endpoint - REST hooks
To install flask use the following command:

```pip install flask```

The script can be started passing an argument - port number on which the endpoint will be accepting connections:

```py http_endpoint.py [port number]```

When RTD is received the timestamp on receipt is recorded to a csv file (receipt_[port number].csv).

#### WebSocket client

```pip install websocket-client```

The FHIR WebSocket endpoint is set in line 34:

``` ws = websocket.WebSocketApp("ws://localhost:8080/websocket", ...```


To run the script use:

```py ws_client.py [SUBID]```

Where [SUBID] is the id of the Subscription resource you generated in the previous step.

When RTD is received the timestamp on receipt is recorded to a csv file (receipt_subscription[SUBID].csv)

#### Generate Observation resources and record timestamps
To generate Observation resources for the patient use the python script "generate_observations.py" in the "fhir_observation" folder. The settings and dependencies are the same as the Subscription generating script:

```py generate_observations.py [PID]```

where [PID] is the id of the Patient resource.

The script generates 1000 resources and records the timestamps to a csv file (generation_timestamps.csv).

Please make sure that the fhir_url is correct and where the generated observations should be sent: to the proxy or directly to the FHIR server.

### Database triggers

Dependencies:

```pip install psycopg2```

The server host, port, credentials and database are set in line 15-19 in the script:

``` connection = psycopg2.connect(user="postgres", password="admin", host="127.0.0.1", port="5432", database="fhir") ```
								  
Once the script is run it is listening for notifications. 

The script takes the filename for the timestamps as an argument.

```py generate_observation [filename]```

When RTD is received the timestamp on receipt is recorded to a csv file ([filename].csv)

### Reverse proxy



Install Golang (https://go.dev/doc/install).

To set up you FHIR server address you need to change line 72:

```rev_proxy, err := NewProxy("http://localhost:8080")```

The address of the reverse proxy is set in line 77:

```log.Fatal(http.ListenAndServe(":5000", nil))```

The address of the RTD recipient http endpoint is defined in line 56:

```go f("http://localhost:5001/",jsonData)```

You can use the python "http_endpoint.py" in "rtd_recipient".

# All these implementations do not include any encryption and are provided only for testing purposes.
