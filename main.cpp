/*
   Basic.cpp: MPU6050 basic example

   Copyright (C) 2018 Simon D. Levy

   Adapted from https://github.com/kriswiner/MPU6050/blob/master/MPU6050BasicExample.ino

   This file is part of MPU.

   MPU is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   MPU is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with MPU.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "gpio.h"
#include "MPU6050.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <math.h>
#include <iostream>
#define timerPeriod 50

static const MPUIMU::Gscale_t GSCALE = MPUIMU::GFS_250DPS;
static const MPUIMU::Ascale_t ASCALE = MPUIMU::AFS_2G;


static MPU6050 imu(ASCALE, GSCALE);

int timer = 0;

static void error(const char * errmsg)
{
	fprintf(stderr, "%s\n", errmsg);
	exit(1);
}

// defined in main.cpp
void delay(uint32_t msec);
uint32_t millis(void);

int main ()
{

	static float temperature;
	static float ax, ay, az;
	static float gx, gy, gz;



	Gpio::initialize();
	Gpio::pinMode(19, GPD_OUTPUT);
	Gpio::pinMode(18, GPD_OUTPUT);

	Gpio::pinMode(17, GPD_OUTPUT);

	Gpio::pinMode(16, GPD_OUTPUT);
	Gpio::pinMode(15, GPD_OUTPUT);



	switch (imu.begin(0)) {

	case MPUIMU::ERROR_IMU_ID:
		error("Bad device ID");
	case MPUIMU::ERROR_SELFTEST:
		error("Failed self-test");
	default:
		printf("MPU6050 online!\n");
	}

	int rightforwardmotorpercentage = 10; //0 is completed off, 1000 is completed on,
	int leftforwardmotorpercentage = 10;


	delay(1000);


	while (1)
	{

	int rightforwarddutycycle = timerPeriod/(timerPeriod*rightforwardmotorpercentage/100);
	int leftforwarddutycycle =  timerPeriod/(timerPeriod*leftforwardmotorpercentage/100);
	std::cout << rightforwarddutycycle << std::endl;

		if (timer > timerPeriod) //sets a 50 ms timer period
			timer = 0;

		if ( timer % 5 == 0 ) //every x miliseconds do something
		{
			// If data ready bit set, all data registers have new data
			if (imu.checkNewData()) {  // check if data ready interrupt

				imu.readAccelerometer(ax, ay, az);

				imu.readGyrometer(gx, gy, gz);

				temperature = imu.readTemperature();

				if (gz > 5)
				{
					

				}
				else if (gz < -5)
				{
					

				}

				else
				{
					
				}


			}

     // Print acceleration values in milligs!
        printf("\nX-acceleration: %f mg ", 1000*ax);
        printf("Y-acceleration: %f mg ", 1000*ay);
        printf("Z-acceleration: %f mg\n", 1000*az);

        // Print gyro values in degree/sec
        printf("X-gyro rate: %4.1f degrees/sec  ", gx);
        printf("Y-gyro rate: %4.1f degrees/sec  ", gy);
        printf("Z-gyro rate: %4.1f degrees/sec\n", gz);
	printf("Right Motor Delay: %i\n", rightforwardmotorpercentage);
printf("Left Motor Delay: %i\n", leftforwardmotorpercentage);


        // Print temperature in degrees Centigrade      
printf("Temperature is %2.2f degrees C\n", temperature);


		}

		if (timer == 1000 )
		{
			Gpio::digitalWrite(19, 1);//turn gpio on
			Gpio::digitalWrite(18, 0);//turn gpio on
		}
		else
		{
			Gpio::digitalWrite(19, 0);//turn gpio on
			Gpio::digitalWrite(18, 0);//turn gpio on
		}

		if (timer == 1000)
		{
			Gpio::digitalWrite(15, 1);//turn gpio on
			Gpio::digitalWrite(16, 0);//turn gpio on
		}
		else
		{
			Gpio::digitalWrite(15, 0);//turn gpio on
			Gpio::digitalWrite(16, 0);//turn gpio on
		}











		timer++;
		delay(1);

	}
}

