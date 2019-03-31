
# Start with a basic flask app webpage.
from flask import Flask, render_template, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit
from time import sleep
import datetime
import pandas as pd
from threading import Thread, Event


# author of the skeleton code
__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#initialize GPIO
import RPi.GPIO as GPIO
from time import sleep     # this lets us have a time delay (see line 15)
input_port = 12
output_port = 13
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
GPIO.setup(input_port, GPIO.IN, pull_up_down=GPIO.PUD_OFF)    # set GPIO12 as input (button)
GPIO.setup(output_port, GPIO.OUT)   # set GPIO13 as an output (LED)

#initialize the haptics

import board
import busio
import adafruit_drv2605

haptics = True

try:
    i2c = busio.I2C(board.SCL, board.SDA)
    drv = adafruit_drv2605.DRV2605(i2c)
    drv.sequence[0] = adafruit_drv2605.Effect(47)
except ValueError as e:
    print(e)
    haptics = False


#create thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 0.01
        super(RandomThread, self).__init__()

    def countButtonPush(self):
        lastButtonState = 0
        number = -1
        dict = {}
        try:
            # this will carry on until you hit CTRL+C
            while not thread_stop_event.isSet():
                #register button push
                if GPIO.input(input_port) != lastButtonState:
                    lastButtonState = GPIO.input(input_port)
                    print( "Button Tranition Detected")
                    if lastButtonState == 1:
                        #haptics
                        if(haptics == True):
                            drv.play()
                        #increase counter by 1
                        number = number +1
                        # sending number to the client
                        socketio.emit('newnumber', {'number': number}, namespace='/test')
                        print(number)
                        GPIO.output(output_port, 1)

                        #update dict with new count and time
                        time = datetime.datetime.now()
                        dict[time] = number
                        count_df = pd.DataFrame.from_dict(dict, orient='index')
                        count_df.to_csv('data/box1_data.csv')
                        # print(count_df)

                else:
                    print("Port 25 is 0/LOW/False - LED OFF")
                    GPIO.output(output_port, 0)         # set port/pin value to 0/LOW/False
                sleep(self.delay)        # wait 0.1 seconds
        finally:                   # this block will run no matter how the try block exits
            GPIO.cleanup()         # clean up after yourself

    def run(self):
        self.countButtonPush()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
