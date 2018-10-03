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

    def forward(self):
        print('forward')
        print(self._motor_calibrate_l)
        print(self._motor_calibrate_r)
        pwmMotor(self.left_motor_f, 200, self._motor_calibrate_l)
        pwmMotor(self.right_motor_f, 200, self._motor_calibrate_r)
        pwmMotor(self.left_motor_r, 200, 0)
        pwmMotor(self.right_motor_r, 200, 0)


    def calibrate(self, v):
        print('it works')
        print(v)
        if int(v) > 100: #slow down right wheel
            self._motor_calibrate_r = 100-(int(v)-100)
            self._motor_calibrate_l = 100
        else:
             self._motor_calibrate_l = 100-(100-int(v)) 
             self._motor_calibrate_r = 100  
         


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
