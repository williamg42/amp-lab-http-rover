from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def controller():
    return render_template('controller.html')

@app.route('/api/control/<direction>')
def api_control(direction=None):
    if direction == 'forward':
        pass
    elif direction == 'left':
        pass
    elif direction == 'right':
        pass
    elif direction == 'stop':
        pass
    else:
        return ('', 400)
    return ('', 204)

def main():
    app.run(host='0.0.0.0', port=8000, threaded=False, debug=False)

if __name__ == '__main__':
    main()
