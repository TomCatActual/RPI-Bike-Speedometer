from flask import *
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import time
import json

app = Flask(__name__)
socketio = SocketIO(app)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pulse = 0
distance = 0
rpm = 0.00
speed = 0.00
wheel_c = 1.75
multiplier = 0
LED0 = 23
LED1 = 24
hall = 18
elapse = 0.00
reed = 11

start = time.time()

GPIO.setup(LED0, GPIO.OUT)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(hall, GPIO.IN, pull_up_down = GPIO.PUD_UP)

@app.route("/")
def index():
        return render_template('speedo2.html')

@app.route('/thing')
def thing():
        def read_thing_state():
            while True:
                thing_state = { 'rpm' : get_rpm(),
                                'speed' : get_speed(),
                                'distance' : get_distance(),
                                'elapse' : get_elapse(),
                                'multiplier' : get_multiplier()  }

                yield 'data:{0}\n\n'.format(json.dumps(thing_state))
        return Response(read_thing_state(), mimetype='text/event-stream')


def get_rpm():
    time.sleep(0.05) # delay to reduce CPU load (can be placed in any other functions except get_pulse)
    return rpm

def get_speed():
    if speed < 80 :
        GPIO.output(LED0,False)
        GPIO.output(LED1,False)
    if speed < 90 and speed > 80 :
        GPIO.output(LED0,True)
        GPIO.output(LED1,False)
    if speed < 100 and speed > 90 :
        GPIO.output(LED0,True)
        GPIO.output(LED1,True)
    return speed

def get_distance():
    return distance

def get_elapse():
    return elapse

def get_multiplier():
    return multiplier

def get_pulse(number):
    global elapse,distance,start,pulse,speed,rpm,multiplier
    cycle = 0
    pulse+=1
    cycle+=1
    if pulse > 0:
        elapse = time.time() - start
        pulse -=1
    if cycle > 0:
        distance += wheel_c
        cycle -= 1

    multiplier = 3600/elapse
    speed = (wheel_c*multiplier)/1000
    rpm = 1/elapse *60

    start = time.time()

try:
    if __name__ == '__main__':
        GPIO.add_event_detect(hall,GPIO.FALLING,callback = get_pulse,bouncetime=20)
        socketio.run(app, host='0.0.0.0', port=9000, debug=True)

except KeyboardInterrupt:
    GPIO.cleanup()
