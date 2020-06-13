import threading
import time
import paho.mqtt.client as mqtt


username = "6e811d9c-566c-4cb0-807a-c098b94afb35"
password = "cbb17969-a361-4257-93ef-ef8c7845ce6c"
subs= "0de6c7d2-b2d2-449d-b92d-498bcfc98dc0/1"
client = mqtt.Client()
client.tls_set()
client.tls_insecure_set(True)
client.username_pw_set(username, password)
client.connect("iot.softwaremakeinindia.com", 8883, 60)
    

def on_connect(client, userdata, flag, rc):
    print("Connected", rc, userdata)
        
def on_message(cleint, userdata, message):
    print(message.topic, str(message.payload.decode('utf-8')))


def subscribe(n,on_connect=on_connect,on_message=on_message):
    # threading here 
    client.on_connect = on_connect
    client.on_message = on_message  
    client.subscribe(subs, 0) 
    client.loop_forever()
		
	
def send(r):
    subs= "0de6c7d2-b2d2-449d-b92d-498bcfc98dc0/1"
    client.publish(subs, "Python publish Test")
    time.sleep(5)
    client.publish(subs, "Python publish Test after 5 seconds")
    

t1 = threading.Thread(target=subscribe,args=(1,))
t2 = threading.Thread(target=send,args=(1,))
t1.start() # independent process start .. 
t2.start()

