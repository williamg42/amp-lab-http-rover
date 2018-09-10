#!/bin/bash 

opkg update
opkg install python-light
opkg install python-email
opkg install python-codecs
opkg install python-logging
opkg install python-openssl
opkg install pyOnionGpio

cd /amp-lab-http-rover
wget --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py
chmod +x /root/amp-lab-http-rover/run_server.sh
chmod +x /root/amp-lab-http-rover/collisionflash.sh


