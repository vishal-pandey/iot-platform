import threading
import paho.mqtt.client as mqtt
import requests
import time
import ssl
import os


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
        self.client.publish(self.key+"/"+deviceid, message)
    # =============================================================================
    
    def subscribe(self,topic,on_connect=None,on_message=None):    
        def letsExecute(topic,on_connect=None,on_message=None):
            if on_connect is None:
                def on_connect(client,userdata, flag, rc):
                    print("Connected", rc, userdata)
                self.client.on_connect = on_connect
            else:
                self.client.on_connect = on_connect
            if on_message is None:
                def on_message(client,userdata, message):
                    print(message.topic, str(message.payload.decode('utf-8')))
                self.client.on_message = on_message
            else:
                self.client.on_message = on_message
            self.client.subscribe(self.key+"/"+topic, 0) 
            self.client.loop_forever()
        
        t1 = threading.Thread(target=letsExecute,args=[topic,on_connect,on_message])  
        t1.start()
        # if on_connect is None:
        #     def on_connect(client,userdata, flag, rc):
        #         print("Connected", rc, userdata)
        #     self.client.on_connect = on_connect
        # else:
        #     self.client.on_connect = on_connect
        # if on_message is None:
        #     def on_message(client,userdata, message):
        #         print(message.topic, str(message.payload.decode('utf-8')))
        #     self.client.on_message = on_message
        # else:
        #     self.client.on_message = on_message


        # self.client.subscribe(self.key+"/"+topic, 0) 
        # self.client.loop_start()


ob = IotC("0de6c7d2-b2d2-449d-b92d-498bcfc98dc0") # init with key


ob.subscribe("1")
# print("orr")
# time.sleep(10)
ob.send("1", "This is KShitij ") # enter device id and message


