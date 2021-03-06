import sys
import threading
import time

from motor_controller import MotorController


from bottle import route, run, Bottle
from bottle import template

from bottle import get, static_file


def valmap(x, in_min, in_max, out_min, out_max):
    if ((in_max - in_min) > (out_max - out_min)):
	return (x - in_min) * (out_max - out_min + 1) / (in_max - in_min + 1) + out_min;
    else:
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
    
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
    nPivSpeed =1*nJoyX
    fPivScale = 0.0 if abs(nJoyY)>fPivYLimit else (1.0 - abs(nJoyY)/fPivYLimit)

# Calculate final mix of Drive and Pivot
    nMotMixL = (1.0-fPivScale)*nMotPremixL + fPivScale*( nPivSpeed)
    nMotMixR = (1.0-fPivScale)*nMotPremixR + fPivScale*(-nPivSpeed)

    print(nMotMixL)
    print(nMotMixR)
    controller.Rg = valmap(nMotMixL, -127, 127,-100,100)
    controller.Lg = valmap(nMotMixR, -127, 127,-100,100)
    controller.drive()
    return ('')

@route('/api/control/move')
def api_control():
    controller.drive()
    return ('')




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
