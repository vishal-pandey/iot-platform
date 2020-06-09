import time
import paho.mqtt.client as mqtt
import ssl
import os

username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')

def on_connect(client, userdata, flag, rc):
	print("Connected", rc, userdata)

def on_message(cleint, userdata, message):
	print(message.topic, str(message.payload.decode('utf-8')))

# def on_subscribe(client, userdata, mid, granted_qos):
# 	print(userdata)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
# client.on_subscribe = on_subscribe

client.tls_set()
client.tls_insecure_set(True)
client.username_pw_set(username, password)
client.connect("iot.softwaremakeinindia.com", 8883, 60)
client.publish("test", "Python publish Test")
# client.loop_forever()
# time.sleep(1)