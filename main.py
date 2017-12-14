import sys

#from motor_controller import MotorController

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def controller():
    return render_template('controller.html')

@app.route('/api/control/<direction>')
def api_control(direction=None):
    if direction == 'forward':
        controller.forward()
    elif direction == 'left':
        controller.left()
    elif direction == 'right':
        controller.right()
    elif direction == 'stop':
        controller.stop()
    else:
        return ('', 400)
    return ('', 204)

def main():

    if len(sys.argv) != 3:
        print('Usage: python main.py [left_motor_pin_number] [right_motor_pin_number]')
    else:
        try:
            global controller
            controller = MotorController(int(sys.argv[1]), int(sys.argv[2]))
            app.run(host='0.0.0.0', port=8000, threaded=False, debug=False)
        except ValueError:
            print('Unable to parse command line arguments.')

if __name__ == '__main__':
    main()
