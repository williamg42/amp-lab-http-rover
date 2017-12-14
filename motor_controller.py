from onionGpio import OnionGpio

class MotorController:

    def __init__(self, left_motor_pin, right_motor_pin):
        self.left_motor = OnionGpio(left_motor_pin)
        self.right_motor = OnionGpio(right_motor_pin)
        self.left_motor.setOutputDirection(0)
        self.right_motor.setOutputDirection(0)

    def forward(self):
        self.left_motor.setValue(1)
        self.right_motor.setValue(1)

    def left(self):
        self.left_motor.setValue(1)
        self.right_motor.setValue(0)

    def right(self):
        self.left_motor.setValue(0)
        self.right_motor.setValue(1)

    def stop(self):
        self.left_motor.setValue(0)
        self.right_motor.setValue(0)
