  /* 
   MPU6050.cpp: Implementation of MPU6050 class methods

   Copyright (C) 2018 Simon D. Levy

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

#include "MPU6050.h"


MPU6050::MPU6050(Ascale_t ascale, Gscale_t gscale, uint8_t sampleRateDivisor) : 
    MPU6xx0(ascale, gscale, sampleRateDivisor)
{
}

MPUIMU::Error_t MPU6050::begin(uint8_t bus)
{
    i2c = new I2C(bus, MPU_ADDRESS);

    return MPU6xx0::begin();
}

void MPU6050::writeMPURegister(uint8_t subAddress, uint8_t data)
{
	i2c->write_byte(subAddress, data);
}

void MPU6050::readMPURegisters(uint8_t subAddress, uint8_t count, uint8_t * dest)
{
    i2c->read_length(subAddress, count, dest);
}



