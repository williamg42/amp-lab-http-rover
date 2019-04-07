import os



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

        print(R)
        print(L)
	command = ""
        if L > 0:

            command = "fast-gpio pwm %d %d %d && " % (self.left_motor_f, 50, L)
            command = command + "fast-gpio set %d %d &&" % (self.left_motor_r, 1)
	   	
	elif L < 0:
		
            command = "fast-gpio pwm %d %d %d && " % (self.left_motor_f, 50, abs(L))
            command = command + "fast-gpio set %d %d &&" % (self.left_motor_r, 0)
	else:
	    command = "fast-gpio set %d %d && " % (self.left_motor_f, 0)
            command = command + "fast-gpio set %d %d &&" % (self.left_motor_r, 0)
		
        if R > 0:

            command = command + "fast-gpio pwm %d %d %d && " % (self.right_motor_f, 50, R)
            command = command + "fast-gpio set %d %d" % (self.right_motor_r, 1)
		
	elif R < 0:
		
            command = command+ "fast-gpio pwm %d %d %d && " % (self.right_motor_f, 50, abs(R))
            command = command + "fast-gpio set %d %d" % (self.right_motor_r, 0)
	else:
	    command = command+ "fast-gpio set %d %d && " % (self.right_motor_f, 0)
            command = command + "fast-gpio set %d %d" % (self.right_motor_r, 0)
	print(command)	
	os.system(command) 
