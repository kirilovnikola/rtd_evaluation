import websocket
import _thread
import time
import rel
import sys
import csv

try:
    sub_id = sys.argv[1]
except:
    print("Failed to assign arguments!")
    sys.exit(1)

with open("receipt_subscription"+sub_id+'.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    def on_message(ws, message):
        print(message)
        time_stamp = int(time.time() * 1000)
                

        writer.writerow([time_stamp])

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print("Connection closed (subscription id not recognized)")
        sys.exit()

    def on_open(ws):
        print("Opened connection")

    if __name__ == "__main__":
        ws = websocket.WebSocketApp("ws://localhost:8080/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        try:
            ws.send("bind "+sub_id) #Send fhir bind message with Subscription id
        except:
            print("Problem with bind subscription id")
            sys.exit()
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()