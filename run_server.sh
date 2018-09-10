#!/bin/bash 

cd /root/amp-lab-http-rover-master/
gpioctl dirout-low 19
gpioctl dirout-low 18
gpioctl dirout-low 16
gpioctl dirout-low 15
python ./main.py 19 16 18 15 
