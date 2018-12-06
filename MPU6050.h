  /* 
   MPU6050.h: Class declaration for MPU6050

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

#include "MPU6xx0.h"
#include "I2C.h"
class MPU6050 : public MPU6xx0 {

    public:

        MPU6050(Ascale_t ascale, Gscale_t gscale, uint8_t sampleRateDivisor=0);

        Error_t begin(uint8_t bus=1);

    protected:

        virtual void writeMPURegister(uint8_t subAddress, uint8_t data) override;

        virtual void readMPURegisters(uint8_t subAddress, uint8_t count, uint8_t * dest) override;

    private:

        // Cross-platform support
        I2C *i2c;
}; 

