import os
import signal
import subprocess



class AutonomousController:

    def __init__(self):
        self.Lat = 0
        self.Long = 0
        self.Run = 0
        global proc
        

    def Navigate(self):
        print('Autonomous Navigation Enabled')
	lat = self.Lat
	long = self.Long
        command = "exec ./test.exe %f %f %s %s &" % (37.215043,  -80.444917, lat, long)
        print(command)
	global proc
        proc = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdin=None, stdout=None, stderr=None, close_fds=True)

    def Kill(self):
        print('Kill')
        os.killpg(os.getpgid(proc.pid), signal.SIGINT) 

   

