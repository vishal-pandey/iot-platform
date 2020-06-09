import requests
import time
import paho.mqtt.client as mqtt
import ssl
import os


class IotC():
    apiEndPoint = "https://iot.softwaremakeinindia.com/iot/"
    
    def __init__(self, key):
        self.key = key
        payload = {'key': self.key}
        res = requests.post(self.apiEndPoint, data=payload).json()
        self.username = res['username']
        self.password = res['password']
        
ob = IotC("74425a47-1c19-4b70-88dd-a2facbe778d3")

print(ob.username)
print(ob.password)