#!/bin/bash 

cd /root/amp-lab-http-rover-master/
gpioctl dirout-low 19
gpioctl dirout-low 18
gpioctl dirout-low 16
gpioctl dirout-low 15
fast-gpio set-output 19
fast-gpio set-output 18
fast-gpio set-output 16
fast-gpio set-output 15


iptables -t nat -I PREROUTING --src 0/0 --dst 192.168.3.1 -p tcp --dport 80 -j REDIRECT --to-ports 8000


python ./main.py 19 15 18 16 
