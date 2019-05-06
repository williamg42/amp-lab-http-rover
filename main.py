import sys
import threading
import time
import math
#from motor_controller import MotorController
from mock_motor_controller import MockMotorController
from autonomous_controller import AutonomousController
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

@route('/autonomous/start/<latval>/<longval>')
def api_control(latval=None, longval=None):
    autonomous.lat = latval
    autonomous.long = longval
    autonomous.Run = 1
    autonomous.Navigate()
    return ('')

@route('/autonomous/stop')
def api_autonomousstop():
    autonomous.Run = 0
    autonomous.Kill()
    return ('')

@route('/api/control/drive/<value1>/<value2>')
def api_control(value1=None, value2=None):
  
    controller.Lg = int(round(float(value1)))
    controller.Rg = int(round(float(value2)))
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
    datapayload = '{}:{}:{}'.format(agps_thread.data_stream.lat,agps_thread.data_stream.lon, agps_thread.data_stream.hdop)
    #datapayload = '37.214842:-80.445229:100'
    return datapayload
   



def main():

    if len(sys.argv) != 5:
        print('Usage: python main.py [left_motor_pin_number_forward] [right_motor_pin_number_forward] [left_motor_pin_number_reverse] [right_motor_pin_number_reverse] ')
    else:
        try:
            global autonomous
            global controller
            #controller = MotorController(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
            controller = MockMotorController(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
            autonomous = AutonomousController(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
            run(host='0.0.0.0', port=8000, debug=True)

        except ValueError:
            print('Unable to parse command line arguments.')

if __name__ == '__main__':
    main()
