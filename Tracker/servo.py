#!/usr/bin/python3
import RPi.GPIO as GPIO

# set RPI pins and servo settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)  # pin and hz setting for servo
pwm.start(12.5)


# set intial variable parameters in main script


pitch_hysterysis = 3.0               # % of range where servo does not react and is shut down
pitch = 0.0                          # imported from compass module
zero_offset = 17.0                   # offsets zero so calc does not go negative
print ("Tilt servo is initialized")

# update servo position every "poll_interval" milliseconds from compass module

def SetPosition (servo_output, pitch, pitch_sp, servo_stop=[0]):
    print( "Servo SetPosition Servo_out ", round(servo_output, 2), "Pitch ", pitch,  "Pitch setpt ", pitch_sp)
    #servo_output = compass.output
    pitch = pitch + zero_offset
    pitch_sp = pitch_sp + zero_offset
    if pitch < 0.0:
        pitch = 0.0
    
    if (pitch_sp - pitch) > (pitch_hysterysis)or (pitch - pitch_sp) > (pitch_hysterysis):
        if (servo_stop[0] == 1):
            pwm.start(servo_output)
            servo_stop[0] = 0
            print("Resetting Servo")
            
        else:    
            pwm.ChangeDutyCycle(servo_output)
            #print ("Servo status", servo_stop)
            print(" Setting Servo pitch to: ", round(servo_output, 2))
            
       
    if (pitch_sp - pitch) <= (pitch_hysterysis)and (pitch - pitch_sp) <= (pitch_hysterysis):
    
        servo_stop[0] = 1
        pwm.start(0)
    # return servo stop status to stop PID loop from winding up while within hysterisys range
    return (servo_stop[0])
    
