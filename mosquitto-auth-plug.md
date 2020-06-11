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
mosquitto_src =/root/mosquitto-1.4.4/  
openssldir =/usr/lib/ssl  
```
sudo make
```
For error config.h not found  
Comment that line in files  
```
sudo cp auth-plug.so /etc/mosquitto/
