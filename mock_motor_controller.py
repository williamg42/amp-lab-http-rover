import subprocess

class MockMotorController:

    def __init__(self, left_motor_pin_f, right_motor_pin_f, left_motor_pin_r, right_motor_pin_r):
        self.left_motor_f = (left_motor_pin_f)
        self.right_motor_f = (right_motor_pin_f)
        self.left_motor_r = (left_motor_pin_r)
        self.right_motor_r = (right_motor_pin_r)
        self._motor_calibrate_l = 100
        self._motor_calibrate_r = 100
        self._xvalue = 0
        self._yvalue = 0
        self.Rg = 0
        self.Lg = 0

   

    def forward(self):
        print('forward')
        print(self._motor_calibrate_l)
        print(self._motor_calibrate_r)
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_f), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_f), str(200), str(100)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.left_motor_r), str(0)])
        #subprocess.call(['fast-gpio', 'pwm', str(self.right_motor_r), str(0)])

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
