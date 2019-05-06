import os
import signal
import subprocess



class AutonomousController:

    def __init__(self, left_motor_pin_f, right_motor_pin_f, left_motor_pin_r, right_motor_pin_r):
        self.Lat = 0
        self.Long = 0
        self.Run = 0
        global proc
        

    def Navigate(self):
        print('Autonomous Navigation Enabled')
        command = "exec ./test.exe %d %d %d %d %d %d &" % (42.35, -71.08, 280.2, self.Lat, self.Long, 280.2)
        global proc
        proc = subprocess.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)

    def Kill(self):
        print('Kill')
        proc.kill()

   
