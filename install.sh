#!/bin/bash 

opkg update
opkg install python-light
opkg install python-email
opkg install python-codecs
opkg install python-logging
opkg install python-openssl
opkg install pyOnionGpio
wget --no-check-certificate https://github.com/williamg42/amp-lab-http-rover/archive/master.tar.gz
tar -xvzf master.tar.gz
cd /amp-lab-http-rover
wget --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py

