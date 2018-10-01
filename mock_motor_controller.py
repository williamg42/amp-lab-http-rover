import subprocess

class MockMotorController:

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
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_f), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_f), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_r), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_r), str(0)])

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
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_f), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_f), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_r), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_r), str(0)])


    def right(self):
        print('right')
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_f), str(0), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_f), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_r), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_r), str(0)])

    def stop(self):
        print('stop')

        #.call(['fast-gpio', 'pwm', str(self.left_motor_f), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_f), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_r), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_r), str(0)])

    
    def reverse(self):
        print('reverse')
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_r), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_r), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_f), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_f), str(0)])
