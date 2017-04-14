#!/usr/bin/python3
# Rick Bell Feb 17, 2017

import RPi.GPIO as gpio
import time
#import compass
import config
#import _thread
import sys


# Use for Rasberry Pi's io pins
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(22, gpio.OUT)    # Motor Controller on/off
gpio.setup(23, gpio.OUT)    # Direction
gpio.setup(24, gpio.OUT)    # Step

fast_speed = 0.001          # FAST stepper interval timer
slow_speed = 0.01           # SLOW stepper interval timer
heading_sp = 0              # inital heading is set to Magnetic north
stepper_hysterysis = 2.0    # deadband
stepper_direction = "null"



print ("Stepper Motor configured")

def SetPosition(heading_sp, heading, t_print = time.time()):
    
    stepper_error = round(heading - heading_sp, 2)
    stepper_error1 = round(((heading_sp - heading +360) % 360), 2)
    stepper_error = abs (stepper_error)
    
    
    if (stepper_error > stepper_hysterysis + 4.0):
            speed = fast_speed
    else:
        speed = slow_speed

    if (stepper_error1)> 180:
        stepper_direction = "left"
        if (stepper_error1 >= stepper_hysterysis):
            gpio.output(23, True)
            gpio.output(24, True)
            time.sleep(speed)
            gpio.output(24, False)
            time.sleep(speed)
            
                
    else:
        stepper_direction = "right"
        if (stepper_error >= stepper_hysterysis):
            gpio.output(23, False)  
            gpio.output(24, True)
            time.sleep(speed)
            gpio.output(24, False)
            time.sleep(speed)    
            #step_counter += 1    
            
    config.speed = speed
    config.stepper_direction = stepper_direction
    config.stepper_error = stepper_error
    config.stepper_error1 = stepper_error1
    config.stepper_direction = stepper_direction
    config.stepper_hysterysis = stepper_hysterysis
        
            
                        
    '''                       
    while (stepper_error >= stepper_hysterysis or stepper_error1 >= stepper_hysterysis):
        heading = config.heading
        gpio.output(22, True)
        if (stepper_error > stepper_hysterysis + 3.0):
            speed = fast_speed
        else:
            speed = slow_speed
            
        gpio.output(24, True)
        time.sleep(speed)
        gpio.output(24, False)
        time.sleep(speed)    
        step_counter += 1
        
    
    
  
    print ("Stepper moved ", direction, " ", step_counter, "pulses")
    
    step_counter = 0
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)

if __name__ == "__main__":
    
    print( "Stepper is __main__")
    heading_sp = int(float(sys.argv[1]))
    SetPosition(heading_sp)
    print("Changing heading to your setpoint of ", heading_sp,  " degrees")
    

        
    '''    
