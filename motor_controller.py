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
	self.Rg = 0
	self.Lg = 0
	
  
    def drive(self):

        R = int(self.Rg)
        L= int(self.Lg)

        #print(R)
        #print(L)
   
        if R == 0 and L == 0:

            command = "fast-gpio set %d %d && " % (self.right_motor_f, 0)
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 0)
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command)


        elif R < -98 and L < -98: #if robot is going forward

            
            command = "fast-gpio set %d %d && " % (self.right_motor_f, 1)
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 1)
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command)


        elif R < -98 and L < 0: #if robot is going forward

            
            command = "fast-gpio set %d %d && " % (self.right_motor_f, 1)
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio pwm %d %d %d && " % (self.left_motor_f, 50, abs(L))
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command)

        elif R < 0 and L < -98: #if robot is going forward

            
            command = "fast-gpio pwm %d %d %d && " % (self.right_motor_f, 50, abs(R))
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 1)
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command)


        elif R < 0 and L < 0: #if robot is going forward

            
            command = "fast-gpio pwm %d %d %d && " % (self.right_motor_f, 50, abs(R))
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio pwm %d %d %d && " % (self.left_motor_f, 50, abs(L))
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command)


        elif R > 98 and L < 0: 

            command = "fast-gpio set %d %d && " % (self.right_motor_f, 0)
            command = command + "fast-gpio set %d %d && " % (self.right_motor_r, 1)
            command = command + "fast-gpio pwm %d %d %d && " % (self.left_motor_f, 50, abs(L))
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command) 
           


        elif R > 0 and L < 0: 

            command = "fast-gpio set %d %d && " % (self.right_motor_f, 0)
            command = command + "fast-gpio pwm %d %d %d && " % (self.right_motor_r, 50, R)
            command = command + "fast-gpio pwm %d %d %d && " % (self.left_motor_f, 50, abs(L))
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 0)
            os.system(command) 


        elif R < 0 and L > 98: #if robot is going forward
            command = "fast-gpio pwm %d %d %d && " % (self.right_motor_f, 50, abs(R))
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 0)
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 1)           
            os.system(command) 


        elif R < 0 and L > 0: #if robot is going forward
            command = "fast-gpio pwm %d %d %d && " % (self.right_motor_f, 50, abs(R))
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 0)
            command = command + "fast-gpio pwm %d %d %d &" % (self.left_motor_r, 50, L)           
            os.system(command)       


        elif R > 98 and L > 98: #if robot is going forward
            command = "fast-gpio set %d%d && " % (self.right_motor_f, 1)
            command = command + "fast-gpio set %d %d &&" % (self.right_motor_r, 0)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 0)
            command = command + "fast-gpio set %d %d &" % (self.left_motor_r, 1)           
            os.system(command)       

        else: 

            command = "fast-gpio set %d %d && " % (self.right_motor_f, 0)
            command = command + "fast-gpio pwm %d %d %d &&" % (self.right_motor_r, 50, R)
            command = command + "fast-gpio set %d %d && " % (self.left_motor_f, 0)
            command = command + "fast-gpio pwm %d %d %d &" % (self.left_motor_r, 50, L)           
            os.system(command) 
