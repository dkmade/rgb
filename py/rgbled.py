#defining the RPi's pins as Input / Output
import RPi.GPIO as GPIO

#importing the library for delaying command.
import time
import json

#used for GPIO numbering
GPIO.setmode(GPIO.BCM) 

#closing the warnings when you are compiling the code
GPIO.setwarnings(False)

RUNNING = True

#defining the pins
green = 20
red = 21
blue = 22

#defining the pins as output
GPIO.setup(red, GPIO.OUT) 
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

#choosing a frequency for pwm
Freq = 100

#defining the pins that are going to be used with PWM
RED = GPIO.PWM(red, Freq)  
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

RED.start(0)
GREEN.start(0)
BLUE.start(0)

with open("data.json", "r") as read_file:
    data = json.load(read_file)

print data['rgb1']['r']
print data['rgb1']['g']
print data['rgb1']['b']

RED.ChangeDutyCycle(data['r'])
GREEN.ChangeDutyCycle(data['g'])
BLUE.ChangeDutyCycle(data['b'])



try:
	#we are starting with the loop
	while RUNNING:

            try:
                file = open("data.json", "r")



            except IOError as e:
                print('error')
            else:
                with file:
                    with file:
                        data = json.load(file)

#                         print data['r']
#                         print data['g']
#                         print data['b']

                        RED.ChangeDutyCycle(data['rgb1']['r'])
                        GREEN.ChangeDutyCycle(data['rgb1']['g'])
                        BLUE.ChangeDutyCycle(data['rgb1']['b'])
                        time.sleep(0.1)

except KeyboardInterrupt:
		# the purpose of this part is, when you interrupt the code, it will stop the while loop and turn off the pins, which means your LED won't light anymore
		RUNNING = False
# 		GPIO.cleanup()
