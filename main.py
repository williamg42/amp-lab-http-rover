import sys
import threading
import time
import math
from motor_controller import MotorController
from gps3.agps3threaded import AGPS3mechanism

from bottle import route, run, Bottle
from bottle import template

from bottle import get, static_file, request


agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechan
agps_thread.stream_data()  # From localhost (), or other h
agps_thread.run_thread(5)  # Throttle time to sleep after 



# Static Routes
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")

@get("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/font")

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")

@route('/')
def controller():
    return template('controller.html')


@route('/api/control/drive/<value1>/<value2>')
def api_control(value1=None, value2=None):
    nJoyX =int(round(float(value1)))
    nJoyY = int(round(float(value2)))
    fPivYLimit = 32.0
    fPivScale = 0
    nPivSpeed = 0
    nMotPremixL = 0
    nMotPremixR = 0

 	# Calculate Drive Turn output due to Joystick X input
    if (nJoyY >= 0):
	#x = true_value if condition else false_value
  # Forward
    	nMotPremixL = 127.0 if nJoyX >=0 else (127.0 + nJoyX)
  	nMotPremixR = (127.0 - nJoyX) if nJoyX >=0 else 127.0
  	
    else: 
  # Reverse
  	nMotPremixL = (127.0 - nJoyX) if nJoyX >=0 else 127.0
  	nMotPremixR = 127.0 if nJoyX>=0 else (127.0 + nJoyX)
  	


# Scale Drive output due to Joystick Y input (throttle)
    nMotPremixL = nMotPremixL * nJoyY/128.0
    nMotPremixR = nMotPremixR * nJoyY/128.0

# Now calculate pivot amount
# - Strength of pivot (nPivSpeed) based on Joystick X input
# - Blending of pivot vs drive (fPivScale) based on Joystick Y input
    nPivSpeed =-1*nJoyX
    fPivScale = 0.0 if abs(nJoyY)>fPivYLimit else (1.0 - abs(nJoyY)/fPivYLimit)

# Calculate final mix of Drive and Pivot
    nMotMixL = (1.0-fPivScale)*nMotPremixL + fPivScale*( nPivSpeed)
    nMotMixR = (1.0-fPivScale)*nMotPremixR + fPivScale*(-nPivSpeed)

    print(nMotMixL)
    print(nMotMixR)
    controller.Lg = (nMotMixR - (-127.0)) * ((100.0) - (-100.0)) / ((127.0) - (-127.0)) + (-100.0)
    controller.Rg = (nMotMixL - (-127.0)) * ((100.0) - (-100.0)) / ((127.0) - (-127.0)) + (-100.0) 
    controller.drive()







    return ('')



@route('/api/control/GPS/')
def api_gps():
    print('----------------')
    print(                   agps_thread.data_stream.time)
    print('Lat:{}   '.format(agps_thread.data_stream.lat))
    print('Lon:{}   '.format(agps_thread.data_stream.lon))
    print('Speed:{} '.format(agps_thread.data_stream.speed))
    print('Course:{}'.format(agps_thread.data_stream.track))
    print('----------------')
    datapayload = 'Lat:{} \n Lon:{} \n Speed:{} \n Course:{}'.format(agps_thread.data_stream.lat,agps_thread.data_stream.lon,agps_thread.data_stream.track,agps_thread.data_stream.speed)
    
    return '<p>This will be  new data</p>'
   



def main():

    if len(sys.argv) != 5:
        print('Usage: python main.py [left_motor_pin_number_forward] [right_motor_pin_number_forward] [left_motor_pin_number_reverse] [right_motor_pin_number_reverse] ')
    else:
        try:
            global controller
            controller = MotorController(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
            #controller = MockMotorController(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
            run(host='0.0.0.0', port=8000, debug=True)

        except ValueError:
            print('Unable to parse command line arguments.')

if __name__ == '__main__':
    main()
