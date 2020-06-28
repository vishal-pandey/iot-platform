#!/bin/bash
sudo apt-get update
sudo apt-get install git 
git clone https://github.com/eclipse/paho.mqtt.c.git mqtt
cd mqtt 
sudo apt-get install openssl
sudo apt-get install libssl-dev
make
sudo make install
