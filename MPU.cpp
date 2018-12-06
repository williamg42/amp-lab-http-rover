/* 
   MPU.cpp: Common methods for MPU classes

   Copyright (C) 2018 Simon D. Levy

   Adapted from https://github.com/kriswiner/MPU9250/blob/master/MPU9250_MS5637_AHRS_t3.ino

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

#include "MPU.h"

MPUIMU::MPUIMU(Ascale_t ascale, Gscale_t gscale, uint8_t sampleRateDivisor)
{
    _aScale = ascale;
    _gScale = gscale;
    _sampleRateDivisor = sampleRateDivisor;

    float avals[4] = {2, 4, 8, 16};
    _aRes = getRes(ascale, avals);

    float gvals[4] = {250, 500, 1000, 2000};
    _gRes = getRes(gscale, gvals);

}

float MPUIMU::getRes(uint8_t scale, float vals[4])
{
    return vals[scale] / 32768.f;
}

uint8_t MPUIMU::getId()
{
    return readMPURegister(WHO_AM_I);  // Read WHO_AM_I register for MPU-9250
}

uint8_t MPUIMU::readMPURegister(uint8_t subAddress)
{
    uint8_t data;
    readMPURegisters(subAddress, 1, &data);
    return data;
}

void MPUIMU::readAccelerometer(float & ax, float & ay, float & az)
{
    uint8_t rawData[6];  // x/y/z accel register data stored here

    readMPURegisters(ACCEL_XOUT_H, 6, &rawData[0]);  // Read the six raw data registers into data array

    int16_t x  = ((int16_t)rawData[0] << 8) | rawData[1] ;  // Turn the MSB and LSB into a signed 16-bit value
    int16_t y  = ((int16_t)rawData[2] << 8) | rawData[3] ;  
    int16_t z  = ((int16_t)rawData[4] << 8) | rawData[5] ; 

    // Convert the accleration value into g's
    ax = (float)x*_aRes - _accelBias[0];  
    ay = (float)y*_aRes - _accelBias[1];   
    az = (float)z*_aRes - _accelBias[2];  
}

void MPUIMU::readGyrometer(float & gx, float & gy, float & gz)
{
    uint8_t rawData[6];  // x/y/z gyro register data stored here

    readMPURegisters(GYRO_XOUT_H, 6, &rawData[0]);  // Read the six raw data registers sequentially into data array

    int16_t x = ((int16_t)rawData[0] << 8) | rawData[1] ;  // Turn the MSB and LSB into a signed 16-bit value
    int16_t y = ((int16_t)rawData[2] << 8) | rawData[3] ;  
    int16_t z = ((int16_t)rawData[4] << 8) | rawData[5] ; 

    // Convert the gyro value into degrees per second
    gx = (float)x*_gRes;  
    gy = (float)y*_gRes;  
    gz = (float)z*_gRes; 
}

int16_t MPUIMU::readRawTemperature(void)
{
    uint8_t rawData[2];  // x/y/z gyro register data stored here
    readMPURegisters(TEMP_OUT_H, 2, &rawData[0]);  // Read the two raw data registers sequentially into data array 
    return ((int16_t)rawData[0] << 8) | rawData[1] ;  // Turn the MSB and LSB into a 16-bit value
}

// Function which accumulates gyro and accelerometer data after device initialization. It calculates the average
// of the at-rest readings and then loads the resulting offsets into accelerometer and gyro bias registers.
void MPUIMU::calibrate(void)
{  
    // reset device
    writeMPURegister(PWR_MGMT_1, 0x80); // Write a one to bit 7 reset bit; toggle reset device
    delay(100);

    // get stable time source; Auto select clock source to be PLL gyroscope reference if ready 
    // else use the internal oscillator, bits 2:0 = 001
    writeMPURegister(PWR_MGMT_1, INV_CLK_PLL);  
    writeMPURegister(PWR_MGMT_2, 0x00);
    delay(200);                                    

    // Configure device for bias calculation
    writeMPURegister(INT_ENABLE, 0x00);   // Disable all interrupts
    writeMPURegister(FIFO_EN, 0x00);      // Disable FIFO
    writeMPURegister(PWR_MGMT_1, 0x00);   // Turn on internal clock source
    writeMPURegister(I2C_MST_CTRL, 0x00); // Disable I2C master
    writeMPURegister(USER_CTRL, 0x00);    // Disable FIFO and I2C master modes
    writeMPURegister(USER_CTRL, 0x0C);    // Reset FIFO and DMP
    delay(15);

    // Configure gyro and accelerometer for bias calculation
    writeMPURegister(CONFIG, 0x01);      // Set low-pass filter to 188 Hz
    writeMPURegister(SMPLRT_DIV, _sampleRateDivisor);  // Set sample rate to 1 kHz
    writeMPURegister(GYRO_CONFIG, _gScale << 3);  
    writeMPURegister(ACCEL_CONFIG, _aScale << 3); 

    uint16_t  gyrosensitivity  = 131;   // = 131 LSB/degrees/sec
    uint16_t  accelsensitivity = 16384;  // = 16384 LSB/g

    // Configure FIFO to capture accelerometer and gyro data for bias calculation
    writeMPURegister(USER_CTRL, 0x40);   // Enable FIFO  
    writeMPURegister(FIFO_EN, 0x78);     // Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes in MPU-9150)
    delay(40); // accumulate 40 samples in 40 milliseconds = 480 bytes

    // At end of sample accumulation, turn off FIFO sensor read
    uint8_t data[12]; // data array to hold accelerometer and gyro x, y, z, data
    writeMPURegister(FIFO_EN, 0x00);        // Disable gyro and accelerometer sensors for FIFO
    readMPURegisters(FIFO_COUNTH, 2, &data[0]); // read FIFO sample count
    uint16_t fifo_count = ((uint16_t)data[0] << 8) | data[1];
    uint16_t packet_count = fifo_count/12;// How many sets of full gyro and accelerometer data for averaging

    int32_t gyro_bias[3]  = {0, 0, 0}, accel_bias[3] = {0, 0, 0};
    for (int k=0; k< packet_count; k++) {
        int16_t accel_temp[3] = {0, 0, 0}, gyro_temp[3] = {0, 0, 0};
        readMPURegisters(FIFO_R_W, 12, &data[0]); // read data for averaging
        accel_temp[0] = (int16_t) (((int16_t)data[0] << 8) | data[1]  ) ;  // Form signed 16-bit integer for each sample in FIFO
        accel_temp[1] = (int16_t) (((int16_t)data[2] << 8) | data[3]  ) ;
        accel_temp[2] = (int16_t) (((int16_t)data[4] << 8) | data[5]  ) ;    
        gyro_temp[0]  = (int16_t) (((int16_t)data[6] << 8) | data[7]  ) ;
        gyro_temp[1]  = (int16_t) (((int16_t)data[8] << 8) | data[9]  ) ;
        gyro_temp[2]  = (int16_t) (((int16_t)data[10] << 8) | data[11]) ;

        accel_bias[0] += (int32_t) accel_temp[0]; // Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
        accel_bias[1] += (int32_t) accel_temp[1];
        accel_bias[2] += (int32_t) accel_temp[2];
        gyro_bias[0]  += (int32_t) gyro_temp[0];
        gyro_bias[1]  += (int32_t) gyro_temp[1];
        gyro_bias[2]  += (int32_t) gyro_temp[2];

    }
    accel_bias[0] /= (int32_t) packet_count; // Normalize sums to get average count biases
    accel_bias[1] /= (int32_t) packet_count;
    accel_bias[2] /= (int32_t) packet_count;
    gyro_bias[0]  /= (int32_t) packet_count;
    gyro_bias[1]  /= (int32_t) packet_count;
    gyro_bias[2]  /= (int32_t) packet_count;

    if(accel_bias[2] > 0L) {accel_bias[2] -= (int32_t) accelsensitivity;}  // Remove gravity from the z-axis accelerometer bias calculation
    else {accel_bias[2] += (int32_t) accelsensitivity;}

    // Construct the gyro biases for push to the hardware gyro bias registers, which are reset to zero upon device startup
    data[0] = (-gyro_bias[0]/4  >> 8) & 0xFF; // Divide by 4 to get 32.9 LSB per deg/s to conform to expected bias input format
    data[1] = (-gyro_bias[0]/4)       & 0xFF; // Biases are additive, so change sign on calculated average gyro biases
    data[2] = (-gyro_bias[1]/4  >> 8) & 0xFF;
    data[3] = (-gyro_bias[1]/4)       & 0xFF;
    data[4] = (-gyro_bias[2]/4  >> 8) & 0xFF;
    data[5] = (-gyro_bias[2]/4)       & 0xFF;

    // Push gyro biases to hardware registers
    pushGyroBiases(data);

    // Output scaled gyro biases for display in the main program
    _gyroBias[0] = (float) gyro_bias[0]/(float) gyrosensitivity;  
    _gyroBias[1] = (float) gyro_bias[1]/(float) gyrosensitivity;
    _gyroBias[2] = (float) gyro_bias[2]/(float) gyrosensitivity;

    // Construct the accelerometer biases for push to the hardware accelerometer bias registers. These registers contain
    // factory trim values which must be added to the calculated accelerometer biases; on boot up these registers will hold
    // non-zero values. In addition, bit 0 of the lower byte must be preserved since it is used for temperature
    // compensation calculations. Accelerometer bias registers expect bias input as 2048 LSB per g, so that
    // the accelerometer biases calculated above must be divided by 8.

    int32_t accel_bias_reg[3] = {0, 0, 0}; // A place to hold the factory accelerometer trim biases

    readAccelOffsets(data, accel_bias_reg);
   
    uint32_t mask = 1uL; // Define mask for temperature compensation bit 0 of lower byte of accelerometer bias registers
    uint8_t mask_bit[3] = {0, 0, 0}; // Define array to hold mask bit for each accelerometer bias axis

    for(int k=0; k< 3; k++) {
        if((accel_bias_reg[k] & mask)) mask_bit[k] = 0x01; // If temperature compensation bit is set, record that fact in mask_bit
    }

    // Construct total accelerometer bias, including calculated average accelerometer bias from above
    accel_bias_reg[0] -= (accel_bias[0]/8); // Subtract calculated averaged accelerometer bias scaled to 2048 LSB/g (16 g full scale)
    accel_bias_reg[1] -= (accel_bias[1]/8);
    accel_bias_reg[2] -= (accel_bias[2]/8);

    data[0] = (accel_bias_reg[0] >> 8) & 0xFF;
    data[1] = (accel_bias_reg[0])      & 0xFF;
    data[1] = data[1] | mask_bit[0]; // preserve temperature compensation bit when writing back to accelerometer bias registers
    data[2] = (accel_bias_reg[1] >> 8) & 0xFF;
    data[3] = (accel_bias_reg[1])      & 0xFF;
    data[3] = data[3] | mask_bit[1]; // preserve temperature compensation bit when writing back to accelerometer bias registers
    data[4] = (accel_bias_reg[2] >> 8) & 0xFF;
    data[5] = (accel_bias_reg[2])      & 0xFF;
    data[5] = data[5] | mask_bit[2]; // preserve temperature compensation bit when writing back to accelerometer bias registers

    // Apparently this is not working for the acceleration biases in the MPU-9250
    // Are we handling the temperature correction bit properly?
    // Push accelerometer biases to hardware registers
    //  writeMPURegister(XAOffsetH(), data[0]);
    //  writeMPURegister(XA_OFFSET_L, data[1]);
    //  writeMPURegister(YAOffsetH(), data[2]);
    //  writeMPURegister(YA_OFFSET_L, data[3]);
    //  writeMPURegister(ZAOffsetH(), data[4]);
    //  writeMPURegister(ZA_OFFSET_L, data[5]);

    // Output scaled accelerometer biases for display in the main program
    _accelBias[0] = (float)accel_bias[0]/(float)accelsensitivity; 
    _accelBias[1] = (float)accel_bias[1]/(float)accelsensitivity;
    _accelBias[2] = (float)accel_bias[2]/(float)accelsensitivity;
}

bool MPUIMU::checkNewData(void)
{
    return (bool)(readMPURegister(INT_STATUS) & 0x01);
}

