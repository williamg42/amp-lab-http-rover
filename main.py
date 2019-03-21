import sys
import threading
import time

from motor_controller import MotorController
#from mock_motor_controller import MockMotorController

from bottle import route, run, Bottle
from bottle import template

from bottle import get, static_file


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
    X =int(round(float(value1)))
    Y = int(round(float(value2)))
    V =(100-abs(X)) * (Y/100) + Y
    W= (100-abs(Y)) * (X/100) + X
    R = (V+W) /2
    L= (V-W)/2
    controller.Lg = L
    controller.Rg = R
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
