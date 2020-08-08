#defining the RPi's pins as Input / Output
import RPi.GPIO as GPIO

#importing the library for delaying command.
import time
import json
import datetime

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

RED.ChangeDutyCycle(data['rgb1']['r'])
GREEN.ChangeDutyCycle(data['rgb1']['g'])
BLUE.ChangeDutyCycle(data['rgb1']['b'])



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


                        datetime_on_start = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d ') + data['timeOn'] + ':00', '%Y-%m-%d %H:%M:%S')
                        datetime_on_end   = datetime_on_start + datetime.timedelta(minutes = data['timeOfGradient'])
                        datetime_off_end   = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d ') + data['timeOff'] + ':00', '%Y-%m-%d %H:%M:%S')
                        datetime_off_start   = datetime_off_end - datetime.timedelta(minutes = data['timeOfGradient'])
                        delta_all = data['timeOfGradient'] * 60

                        if (datetime.datetime.now() < datetime_on_start or datetime.datetime.now() > datetime_off_end):
                            RED.ChangeDutyCycle(0)
                            GREEN.ChangeDutyCycle(0)
                            BLUE.ChangeDutyCycle(0)
                        elif(datetime.datetime.now() > datetime_on_start and datetime.datetime.now() < datetime_on_end):
                            delta_now = datetime.datetime.now() - datetime_on_start
                            seconds = delta_now.total_seconds()
                            koef = seconds/delta_all
                            RED.ChangeDutyCycle(data['rgb1']['r']*koef)
                            GREEN.ChangeDutyCycle(data['rgb1']['g']*koef)
                            BLUE.ChangeDutyCycle(data['rgb1']['b']*koef)
                        elif(datetime.datetime.now() > datetime_on_end and datetime.datetime.now() < datetime_off_start):
                            RED.ChangeDutyCycle(data['rgb1']['r'])
                            GREEN.ChangeDutyCycle(data['rgb1']['g'])
                            BLUE.ChangeDutyCycle(data['rgb1']['b'])
                        elif(datetime.datetime.now() > datetime_off_start and datetime.datetime.now() < datetime_off_end):
                            delta_now = datetime.datetime.now() - datetime_off_start
                            seconds = delta_now.total_seconds()
                            koef = 1 - seconds/delta_all
                            RED.ChangeDutyCycle(data['rgb1']['r']*koef)
                            GREEN.ChangeDutyCycle(data['rgb1']['g']*koef)
                            BLUE.ChangeDutyCycle(data['rgb1']['b']*koef)


#                         RED.ChangeDutyCycle(data['rgb1']['r'])
#                         GREEN.ChangeDutyCycle(data['rgb1']['g'])
#                         BLUE.ChangeDutyCycle(data['rgb1']['b'])
                        time.sleep(0.1)

except KeyboardInterrupt:
		# the purpose of this part is, when you interrupt the code, it will stop the while loop and turn off the pins, which means your LED won't light anymore
		RUNNING = False
# 		GPIO.cleanup()
