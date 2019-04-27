#!/bin/bash 

cd /root/amp-lab-http-rover/

gpioctl dirout-low 16
gpioctl dirout-low 15


omega2-ctrl gpiomux set pwm0 pwm
omega2-ctrl gpiomux set pwm1 pwm

iptables -t nat -I PREROUTING --src 0/0 --dst 192.168.3.1 -p tcp --dport 80 -j REDIRECT --to-ports 8000


python ./main.py 19 18 15 16 
