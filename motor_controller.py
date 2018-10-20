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

  
    def drive(self, Xin, Yin):
        
        X =int(round(float(Xin)))
        Y = int(round(float(Yin)))


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

        

