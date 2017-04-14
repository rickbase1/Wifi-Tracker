#!/usr/bin/python3
import sys
import signal
import RPi.GPIO as gpio 
import time

 # Functions

def signal_handler(signal, frame):
    print("Command Interupted.  Only {} steps completed".format(StepCounter))
    # Return running step count
    gpio.output(22, False)
    sys.exit(StepCounter)



# Register function that will handle interupts
signal.signal(signal.SIGINT, signal_handler)


try: 
    direction = sys.argv[1]
    steps = int(float(sys.argv[2]))
    wait_time = float(sys.argv[3])
except:
    direction = 'left' ## new line to set default direction
    steps = 0
 
#print which direction and how many steps 
print("Turning", direction, steps," steps.")



# Use for Rasberry Pi's io pins
gpio.setmode(gpio.BCM)




gpio.setup(22, gpio.OUT)    # Motor Controller on/off
gpio.setup(23, gpio.OUT)    # Direction
gpio.setup(24, gpio.OUT)    # Step

 
 
# Set rotation direction
if direction == 'left':
    gpio.output(23, True)
elif direction == 'right':
    gpio.output(23, False)

 
 

# Keep a running total of the numebr of steps taken
StepCounter = 0
 
#waittime controls speed
#WaitTime = 0.01
WaitTime = wait_time

 
 
# Each pulse to the motor controller corresponds to a single motor step.
# We iterate through the required # of steps 
gpio.output(22, True)
while StepCounter < steps:
 
    #turning the gpio on and off tells the easy driver to take one step
    gpio.output(24, True)
    gpio.output(24, False)
    StepCounter += 1
 
    #Wait before taking the next step...this controls rotation speed
    time.sleep(WaitTime)
#------------------------------------------------------------------------
#------------------------------------------------------------------------
 
gpio.output(22, False) 

gpio.cleanup()
