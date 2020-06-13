
### Install MQTT
```
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

### Publish and subscribe
```
mosquitto_sub -h localhost -t test
mosquitto_pub -h localhost -t test -m "hello world"
```

### Password Protect MQTT
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd uservishal
sudo nano /etc/mosquitto/conf.d/default.conf
```

##### default.conf Content
```
allow_anonymous false
password_file /etc/mosquitto/passwd
```

### Restart MQTT Server
```
sudo systemctl restart mosquitto
mosquitto -d
```

### Publish and subscribe with password
```
mosquitto_sub -h localhost -t test -u "uservishal" -P "password"
mosquitto_pub -h localhost -t "test" -m "hello world" -u "uservishal" -P "password"
```

### MQTT SSL
```
sudo nano /etc/mosquitto/conf.d/default.conf
```

##### default.conf Content
```
...

listener 8883
certfile /etc/letsencrypt/live/mqtt.example.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.example.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.example.com/privkey.pem
```

### Restart MQTT Server
```
sudo systemctl restart mosquitto
```

### Publish Subscribe with SSL
```
mosquitto_pub -h iot.softwaremakeinindia.com -t test -m "hello again" -p 8883 --capath /etc/ssl/certs/ -u "uservishal" -P "password"
mosquitto_sub -h iot.softwaremakeinindia.com -t test -p 8883 --capath /etc/ssl/certs/ -u "uservishal" -P "password"
```

### MQTT Websocket
```
sudo nano /etc/mosquitto/conf.d/default.conf
```

##### default.conf Content
```
...

listener 8083
protocol websockets
certfile /etc/letsencrypt/live/iot.softwaremakeinindia.com/cert.pem
cafile /etc/letsencrypt/live/iot.softwaremakeinindia.com/chain.pem
keyfile /etc/letsencrypt/live/iot.softwaremakeinindia.com/privkey.pem
```

### Restart MQTT Server
```
sudo service mosquitto restart
```

##### MQTT Websocket Client to check
https://www.eclipse.org/paho/clients/js/utility/



## Final Configuration File
```
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

password_file /etc/mosquitto/passwd
allow_anonymous false

listener 8883
certfile /etc/letsencrypt/live/mqtt.softwaremakeinindia.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.softwaremakeinindia.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.softwaremakeinindia.com/privkey.pem

listener 8083
protocol websockets
certfile /etc/letsencrypt/live/mqtt.softwaremakeinindia.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.softwaremakeinindia.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.softwaremakeinindia.com/privkey.pem
```



##### *note - 
it may me needed to restart mosquitto twice due to non availablity of port on restarted