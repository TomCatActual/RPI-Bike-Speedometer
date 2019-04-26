#!/usr/bin/python3
import RPi.GPIO as GPIO
import time, math

pin = 5
count = 0

def calculate_speed(r_cm, time_sec):
    global count
    circ_cm = (2 * math.pi) * r_cm
    rot = count / 2.0
    dist_km = (circ_cm * rot) / 100000.0 # convert to kilometres
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * 3600 # convert to distance per hour
    return km_per_hour * 1.18

def spin(channel):
    global count
    count += 1
    print (count)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(pin, GPIO.FALLING, callback=spin)

interval = 5

while True:
    count = 0
    time.sleep(interval)
    print (calculate_speed(9.0, interval), "kph")

# explanation
There are 2 methods for calculating speed using Python.
The first method is using "pre-defined interval" and the second method is using "calculated interval". Before we dive straight into the code let me show you the setup of this project. What we need are RaspberryPi, hall effect sensor or reed switch and small magnet. You can use either one of the sensor and the code would be pretty much the same.
The hall effect sensor that I'm using is of Unipolar type. Depending on how you setup the magnet on the spinning mechanism, it will decide which type of hall sensor is suitable for you. Unipolar sensor can only get triggered on one side of the sensor. Bipolar sensor has the ability to detect magnet in both directions✌🏻️

Reed sensor is a much simpler device to use for this project . I will show you how to use both sensors😬
As this project is just a prototype for the wheel of our motorcycle/car,  I'm using a cpu fan as a replacement for the real wheel.
The magnet is mounted on the flat surface of the fan.

Hall effect sensor has 3 pins or legs. There are VCC, Ground and Output.
 Connect the VCC to 5V  .
 Ground as usual.
 And output to any  GPIO that you wish. If everything is connected, you are good to go.

CALCULATED INTERVAL METHOD

Using calculated interval method is better and more people precise compared to pre-defined interval.
Here, we make use of the time.time() module in Python to precisely measure time duration of each interrupt interval.
We are using add_event_detect() to take advantage of the GPIO pin interrupt.
Here we use one callback function called "calculate_elapse(channel)". This function will get called anytime the interrupt happens.

TRY to grab this concept in order to understand this code. We are using ONE magnet mounted on the spoke and ONE hall effect sensor
mounted on a static surface on our fan chassis
Therefore, we could come up with an assumption that 1 complete rotation will be made whenever 1 interrupt event occurs.

From that assumption, we could determine the time duration of 1 complete rotation in our callback function.
So, lets take a look at the callback function in the code. It is named "calculate_elapse(channel)". In that function, we have
3 main global variables. Global variables are made so that their values can be used outside that local function which
in case, our local variable is our callback function named "calculate_elapse(channel)". They are:

- pulse
- start_timer
- elapse

1) pulse : a counter variable used to count the number of interrupts. it can also be used to calculate total distance travelled
by the wheel.
2) start_timer : a time variable that stores the initial timestamp before an interrupt occurs and stores the current timestamp
after the interrupt has occurred!
3) elapse : time duration of 1 complete rotation by subtracting the timestamp during interrupt instance with start_timer which holds
the initial timestamp before that interrupt occurred.

After we have calculated the elapse, we immediately set our new start_timer with the current timestamp so that it can be used to
calculate our next elapse value if new interrupt occurs.

Now that we have our global elapse value, we can move on to next function which is "calculate_speed(r_cm)". this function will be called
in our main loop. This function takes in one parameter which is the radius of wheel in centimeter (you could use meter if you wish).
As the global elapse value is now accessible in this function, we can calculate the speed of the wheel using simple mathematical
formula.

First, we have to make sure that our elapse value is not Zero to avoid DivisionByZero error.
Round Per Minute (rpm) can be calculated using : rpm = 1/elapse * 60
where 1 is referring to 1 complete rotation and 60 is referring to 60 seconds.

circ_cm (wheel circumference) can be calculated using : 2 x pi x radius

dist_km (distance moved in km) can be calculated using : dist_km = circ_cm/100000

km_per_sec (speed in KM/s) calculate using: km_per_sec =  dist_km / elapse

km_per_hour (speed in KM/h) calculate using: km_per_hour =  km_per_sec * 3600

That's all for the CALCULATED INTERVAL METHOD! You can try it with your Raspberry Pi and get the result printed on the terminal.
