#!/bin/bash 

opkg update
opkg install python
opkg install python-pip
pip install gps3

cd root/amp-lab-http-rover/
wget --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py
chmod +x ./run_server.sh
chmod +x ./collisionflash.sh
rm -r /etc/rc.local
cp ./rc.local /etc/rc.local
cp ./Dependancies/Boostlibs/libboost_filesystem.so.1.68.0 /usr/lib
cp ./Dependancies/Boostlibs/libboost_system.so.1.68.0 /usr/lib
cp ./Dependancies/src/PWM.exe ./
chmod u+x ./PWM.exe
rm -r /etc/dnsmasq.conf
cp ./dnsmasq.conf /etc/dnsmasq.conf

