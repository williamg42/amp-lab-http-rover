import sys

from motor_controller import MotorController

from flask import Flask
from flask import render_template

app = Flask(__name__)

try:
    controller = MotorController(sys.argv[1], sys.argv[2])
except:
    print('Usage: python main.py 1 2')
    sys.exit(1)

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
    app.run(host='0.0.0.0', port=8000, threaded=False, debug=False)

if __name__ == '__main__':
    main()
