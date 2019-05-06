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
        command = "exec ./test.exe %d %d %d %d %d %d &" % (37.215043,  -80.444917, 280.2, self.Lat, self.Long, 280.2)
        global proc
        proc = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdin=None, stdout=None, stderr=None, close_fds=True)

    def Kill(self):
        print('Kill')
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM) 

   

