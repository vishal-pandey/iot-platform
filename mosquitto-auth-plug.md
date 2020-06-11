### Build and Install Mosquitto Auth Plug for mysql
```
wget https://mosquitto.org/files/source/mosquitto-1.4.15.tar.gz
tar -xvf mosquitto-1.4.15.tar.gz
git clone https://github.com/jpmens/mosquitto-auth-plug.git

sudo apt-get install build-essential
sudo apt-get install libc-ares-dev
sudo apt-get install uuid-dev
sudo apt-get install libssl-dev
sudo apt-get install openssl
sudo apt-get install libcurl4-openssl-dev

cd mosquitto-1.4.15  
nano config.mk  
```
with_srv:=no  
```
sudo make binary
sudo make install

cd ../mosquitto-auth-plug
cp config.mk.in config.mk
nano config.mk
```
mosquitto_src =/home/ubuntu/mosquitto-1.4.15  
openssldir =/usr/lib/ssl  
```
sudo make
```
For error config.h not found  
Comment that line in files  
```
sudo cp auth-plug.so /etc/mosquitto/
```

##### mosquitto.conf
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
certfile /etc/letsencrypt/live/mqtt.example.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.example.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.example.com/privkey.pem

listener 8083
protocol websockets
certfile /etc/letsencrypt/live/mqtt.example.com/cert.pem
cafile /etc/letsencrypt/live/mqtt.example.com/chain.pem
keyfile /etc/letsencrypt/live/mqtt.example.com/privkey.pem



# Auth Plugin

auth_plugin /etc/mosquitto/auth-plug.so
auth_opt_backends mysql
auth_opt_host localhost
auth_opt_port 3306
auth_opt_dbname mqtt
auth_opt_user root
auth_opt_pass password
auth_opt_userquery SELECT pw FROM users WHERE username = '%s'
auth_opt_superquery SELECT IFNULL(COUNT(*), 0) FROM users WHERE username = '%s' AND super = 1
auth_opt_aclquery SELECT topic FROM acls WHERE username = '%s'


# Usernames with this fnmatch(3) (a.k.a glob(3))  pattern are exempt from the
# module's ACL checking
auth_opt_superusers S*
```

