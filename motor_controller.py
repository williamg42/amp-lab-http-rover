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


    def drive(self):
        print('driving')
        X = self._xvalue
        Y = self._yvalue


        V =(100-abs(X)) * (Y/100) + Y
        W= (100-abs(Y)) * (X/100) + X
        R = (V+W) /2
        L= (V-W)/2
   


        print(R)
        print(L)

        if R < 0: #if robot is going forward

            pwmMotor(self.right_motor_f, 200, abs(R))
            pwmMotor(self.right_motor_r, 200, 0)           

        else: 

            pwmMotor(self.right_motor_f, 200, 0)
            pwmMotor(self.right_motor_r, 200, R)  


        if L < 0: #if robot is going forward

            pwmMotor(self.left_motor_f, 200, abs(L))
            pwmMotor(self.left_motor_r, 200, 0)           

        else: 

            pwmMotor(self.left_motor_f, 200, 0)
            pwmMotor(self.left_motor_r, 200, L)  



        


    def calibratex(self, v1):
        self._xvalue = (round(float(v1)))

    def calibratey(self, v2):
        print('it works')
        print(v2)
        self._yvalue = (round(float(v2)))
                     


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
