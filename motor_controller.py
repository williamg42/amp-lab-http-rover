from onionGpio import OnionGpio

class MotorController:

    def __init__(self, left_motor_pin_f, right_motor_pin_f, left_motor_pin_r, right_motor_pin_r):
        self.left_motor_f = OnionGpio(left_motor_pin_f)
        self.right_motor_f = OnionGpio(right_motor_pin_f)
        self.left_motor_r = OnionGpio(left_motor_pin_r)
        self.right_motor_r = OnionGpio(right_motor_pin_r)
        self.left_motor_f.setOutputDirection(0)
        self.right_motor_f.setOutputDirection(0)
        self.left_motor_r.setOutputDirection(0)
        self.right_motor_r.setOutputDirection(0)

    def forward(self):
        self.left_motor_f.setValue(1)
        self.right_motor_f.setValue(1)
        self.left_motor_r.setValue(0)
        self.right_motor_r.setValue(0)

    def left(self):
        self.left_motor_f.setValue(1)
        self.right_motor_f.setValue(0)
        self.left_motor_r.setValue(0)
        self.right_motor_r.setValue(0)

    def right(self):
        self.left_motor_f.setValue(0)
        self.right_motor_f.setValue(1)
        self.left_motor_r.setValue(0)
        self.right_motor_r.setValue(0)

    def stop(self):
        self.left_motor_f.setValue(0)
        self.right_motor_f.setValue(0)
        self.left_motor_r.setValue(0)
        self.right_motor_r.setValue(0)
        
    def reverse(self):
        self.left_motor_f.setValue(0)
        self.right_motor_f.setValue(0)
        self.left_motor_r.setValue(1)
        self.right_motor_r.setValue(1)        
