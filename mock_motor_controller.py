class MockMotorController:

    def __init__(self, left_motor_pin, right_motor_pin):
        self.left_motor = left_motor_pin
        self.right_motor = right_motor_pin

    def forward(self):
        print('forward')

    def left(self):
        print('left')

    def right(self):
        print('right')

    def stop(self):
        print('stop')
    
    def reverse(self):
        print('reverse')
