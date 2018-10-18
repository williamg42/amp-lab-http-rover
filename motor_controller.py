import os

def pwmMotor(pin, frequency, dutyCyclePercentage):
	# create a string to hold our command line code,assign the function arguments to fast-gpio command arguments
    command = "fast-gpio pwm %d %d %d" % (pin, frequency, dutyCyclePercentage)
	# execute the command using the OS
    os.system(command)

class MotorController:
    
    def __init__(self, left_motor_pin_f, right_motor_pin_f, left_motor_pin_r, right_motor_pin_r):
        self.left_motor_f = (left_motor_pin_f)
        self.right_motor_f = (right_motor_pin_f)
        self.left_motor_r = (left_motor_pin_r)
        self.right_motor_r = (right_motor_pin_r)
        self._motor_calibrate_l = 100
        self._motor_calibrate_r = 100
        self._xvalue = 0
        self._yvalue = 0

    def forward(self):
        print('forward')
        print(self._motor_calibrate_l)
        print(self._motor_calibrate_r)
        pwmMotor(self.left_motor_f, 200, self._motor_calibrate_l)
        pwmMotor(self.right_motor_f, 200, self._motor_calibrate_r)
        pwmMotor(self.left_motor_r, 200, 0)
        pwmMotor(self.right_motor_r, 200, 0)


    def calibratex(self, v1):
        print('it works')
        print(v1)
        if float(v1) > 0: #slow down right wheel
            self._motor_calibrate_r = float(self._xvalue)-(float(v1))
            self._motor_calibrate_l = float(self._xvalue)
        else:
             self._motor_calibrate_l = float(self._xvalue)+(float(v1)) 
             self._motor_calibrate_r = float(self._xvalue)  

    def calibratey(self, v2):
        print('it works')
        print(v2)
        self._xvalue = float(v2)
                     


    def left(self):
        print('left')
        pwmMotor(self.left_motor_f, 200, 0)
        pwmMotor(self.right_motor_f, 200, 100)
        pwmMotor(self.left_motor_r, 200, 0)
        pwmMotor(self.right_motor_r, 200, 0)


    def right(self):
        print('right')
        pwmMotor(self.left_motor_f, 200, 100)
        pwmMotor(self.right_motor_f, 200, 0)
        pwmMotor(self.left_motor_r, 200, 0)
        pwmMotor(self.right_motor_r, 200, 0)

    def stop(self):
        print('stop')

        pwmMotor(self.left_motor_f, 200, 0)
        pwmMotor(self.right_motor_f, 200, 0)
        pwmMotor(self.left_motor_r, 200, 0)
        pwmMotor(self.right_motor_r, 200, 0)
    
    def reverse(self):
        print('reverse')
        pwmMotor(self.left_motor_f, 200, 0)
        pwmMotor(self.right_motor_f, 200, 0)
        pwmMotor(self.left_motor_r, 200, self._motor_calibrate_r)
        pwmMotor(self.right_motor_r, 200, self._motor_calibrate_l)
