
"""
Demo Flask application to test the operation of Flask with socket.io
Aim is to create a webpage that is constantly updated with random numbers from a background python process.
30th May 2014
===================
Updated 13th April 2018
+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources
"""




# Start with a basic flask app webpage.
from flask import Flask, render_template, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from threading import Thread, Event

#impor


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
GPIO.setup(input_port, GPIO.IN, pull_up_down=GPIO.PUD_OFF)    # set GPIO25 as input (button)
GPIO.setup(output_port, GPIO.OUT)   # set GPIO24 as an output (LED)
lastButtonState = 0

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 0.01
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        number = 0
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        # print("Making random numbers")
        # while not thread_stop_event.isSet():
        #     number = round(random()*10, 3)
        #     print(number)
        #     socketio.emit('newnumber', {'number': number}, namespace='/test')
        #     sleep(self.delay)

        try:
            while not thread_stop_event.isSet():         # this will carry on until you hit CTRL+C
                if GPIO.input(input_port) != lastButtonState: # if port 25 == 1
                    lastButtonState = GPIO.input(input_port)
                    print( "button Tranition Detected")
                    if lastButtonState == 1:
                        number = number +1
                        socketio.emit('newnumber', {'number': number}, namespace='/test')
                        print(number)
                        GPIO.output(output_port, 1)         # set port/pin value to 1/HIGH/True
                else:
                    print("Port 25 is 0/LOW/False - LED OFF")
                    GPIO.output(output_port, 0)         # set port/pin value to 0/LOW/False
                sleep(self.delay)        # wait 0.1 seconds

        finally:                   # this block will run no matter how the try block exits
            GPIO.cleanup()         # clean up after yourself

    def run(self):
        self.randomNumberGenerator()


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
