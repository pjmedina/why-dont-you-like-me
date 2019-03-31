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


try:
    i2c = busio.I2C(board.SCL, board.SDA)
    drv = adafruit_drv2605.DRV2605(i2c)
    drv.sequence[0] = adafruit_drv2605.Effect(47)
except ValueError as e:
    haptics = False

lastButtonState = 0
while True
    #register button push
    if GPIO.input(input_port) != lastButtonState:
    	lastButtonState = GPIO.input(input_port)
    	print( "Button Tranition Detected")
		if lastButtonState == 1:
		#haptics
		if(haptics == True):
			drv.play()