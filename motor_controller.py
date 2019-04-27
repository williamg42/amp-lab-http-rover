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
	command = "./PWM.exe %d %d &" % (L, R)
	print(command)	
	os.system(command) 
