#!/bin/bash 

opkg update
opkg install python-light
opkg install python-email
opkg install python-codecs
opkg install python-logging
opkg install python-openssl
opkg install pyOnionGpio
rm -r /root/master.tar.gz
cd root/amp-lab-http-rover-master/
wget --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py
chmod +x ./run_server.sh
chmod +x ./collisionflash.sh
rm -r /etc/rc.local
cp ./rc.local /etc/rc.local
rm -r /etc/dnsmasq.conf
cp ./dnsmasq.conf /etc/dnsmasq.conf

