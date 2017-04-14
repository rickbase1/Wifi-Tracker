import RPi.GPIO as GPIO
#import time
#import pickle
#import os
#import json
#import PID


# set RPI pins and servo settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)

# set intial variable parameters
# poll_interval = 1000             # in milliseconds
zero_pos = 4.00                       # use to set min position of servo
max_pos = 20.00                     # use to set max position of servo
servo_position = 50.0              # in % of range, adjust to change initial midpoint of tilt servo
                                                # value comes from main "tracker" module PID loop                       
servo_output = 12.0                # default servo frequency output
pitch_hysterysis = 5                 # % of range where servo does not react and is shut down
pitch_sp = 0.0                          # manually set in GUI
pitch = 0.0                               # imported from compass module
zero_offset = 20.0                    # offsets zero so calc does not go negative

# update servo position every "poll_interval" milliseconds
class SERVO:

    #t_interval = time.time()
    #compass_data = pickle.load( open("compass_data.p", "rb"))
    
    #from compass import compass_retrieve
    #compass_data = json.loads(os.environ["COMPASS_DATA"])
    #compass_data = compass_retrieve()
    
    def SetPosition (pitch):
        pitch = pitch + zero_offset
        if pitch < 0.0:
            pitch = 0.0

    #print (compass_data) # 0 = heading, 1 = yaw, 2 = pitch)
    #pitch = compass_data[2]
    
        servo_position = pitch / 40.0 * 100.0
    # scaling of variables
        
        servo_output = servo_position / (max_pos - zero_pos) + zero_pos
    

       
        if (pitch - pitch_sp) < (pitch_hysterysis):
            pwm.start(10)
            pwm.ChangeDutyCycle(servo_output)
            #print(" moving antenna back")
          
          
        elif (pitch - pitch_sp) > (pitch_hysterysis):
            pwm.start(10)
            pwm.ChangeDutyCycle(servo_output)
            #print("Moving antenna ahead")

        else:
            pwm.stop()

        #compass_data = pickle.load( open("compass_data", "rb"))


    #if __name__ == "__main__":
        
        
    #time.sleep(poll_interval*1.0/1000.0)
