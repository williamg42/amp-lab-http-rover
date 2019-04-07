#!/bin/bash 

opkg update
opkg install python
opkg install python-email
opkg install python-codecs
opkg install python-logging
opkg install python-openssl
opkg install pyOnionGpio
opkg install python-pip
rm -r /root/Joystick.tar.gz
cd root/amp-lab-http-rover/
wget --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py
chmod +x ./run_server.sh
chmod +x ./collisionflash.sh
rm -r /etc/rc.local
cp ./rc.local /etc/rc.local
rm -r /etc/dnsmasq.conf
cp ./dnsmasq.conf /etc/dnsmasq.conf

