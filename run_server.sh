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



python ./main.py 19 15 18 16 
