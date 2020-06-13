import threading
import paho.mqtt.client as mqtt
import requests
import time
import ssl
import os
""" 
"""


def on_connect(client,userdata, flag, rc):
    print("Connected", rc, userdata)
        
def on_message0(client,userdata, message):
    print(message.topic, str(message.payload.decode('utf-8')))

class IotC():
    apiEndPoint = "https://iot.softwaremakeinindia.com/iot/"
    #-------------------------------INIT------------------------------------------
    def __init__(self, key):                                                 
        self.key = key
        payload = {'key': self.key}
        res = requests.post(self.apiEndPoint, data=payload).json()
        self.username = res['username']
        self.password = res['password']
                
        self.client = mqtt.Client()
        
        self.client.tls_set()
        self.client.tls_insecure_set(True)
        self.client.username_pw_set(self.username, self.password)
        self.client.connect("iot.softwaremakeinindia.com", 8883, 60)
        
        
    # ------------------------------------------------------------------------------ 

    # ________________________ SEND _______________________________________________
    def send(self, deviceid, message):
        self.client.publish(self.key+"/"+deviceid, "this is for testing")
    # =============================================================================
    
    def subscribe(self,topic,on_connect=on_connect,on_message=on_message):
        self.cleint.on_connect = on_connect
        self.client.on_message = on_message
        self.client.subscribe(self.key+"/"+topic, 0) 




ob = IotC("0de6c7d2-b2d2-449d-b92d-498bcfc98dc0") # init with key
ob.send("1", "This is testing") # enter device id and message
# ob.subscribe("1")


