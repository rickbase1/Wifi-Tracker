import sys

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import RPi.GPIO
#import socket
import os
from PID import PID



# disable GPIO warning messages

RPi.GPIO.setwarnings(False)

# discover IMU




SETTINGS_FILE = "RTIMULib"

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
print (s)
print (imu)

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")
else:
   print("Settings File " + SETTINGS_FILE + " found")
   
# offsets
yawoff = 0.0
pitchoff = 0.0
rolloff = 0.0

# timers
t_print = time.time()
t_damp = time.time()
t_fail = time.time()
t_fail_timer = 0.0
t_shutdown = 0

# check IMU initialization status

if (not imu.IMUInit()):
    print("MPU9250 IMU magnemometer failed to initialize on i2c bus")
    sys.exit(1)
else:
    print("MPU9250 IMU Init Succeeded");

    
# confiure IMU parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Poll interval retreived and set to ", poll_interval, " milliseconds")

if imu.getCompassCalibrationEllipsoidValid():
    print("Compass is using Ellipsoid data")

if imu.getCompassCalibrationValid():
    print("compass is using min/max data")


# Configure servo parameters

RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM) # set pins to Broadcom output not RPI board
RPi.GPIO.setup(18, RPi.GPIO.OUT) # set pin 18 as an output
# pwm.setPWM(0,0,100
pwm = RPi.GPIO.PWM(18, 50) # set as PWM class 18
pwm.start(5) # set duty cycle

# initialize data variables

roll = 0.0
pitch = 0.0
yaw = 0.0
heading = 0.0
rollrate = 0.0
pitchrate = 0.0
pitch_sp = 0            # centers Y axis servo
pitch_sp1 = 0.0         # scaled servo setpt
pitch_hysterysis = 1.0    # variance allowed for Y axis control
x = 0.0                 # pitch interval timer
x1 = 0.00    # test output of PID
u1 = 0.0
y = 0.0000
yc = 0.0000
integral = 0.00
derivitive = 0.000
output = 0.00
u = 0.0                 # PID loop output
yawrate = 0.0



# magnetic deviation
# use file "mag" in current directory to set offset
# todo, get offset based on geolocate data from nooa tables

f = open('mag', 'r')
magnetic_deviation = float(f.readline())
print("Magnetic Deviation is ", magnetic_deviation)
f.close()

# dampening variables
t_one = 0
t_three = 0
roll_total = 0.0
roll_run = [0] * 10
heading_cos_total = 0.0
heading_sin_total = 0.0
heading_cos_run = [0] * 30
heading_sin_run = [0] * 30


#------------------------------------------------------------------------------------------------------
'''def pid_controller(y, yc, h=1.000, Ti=1.00, Td=10.0, Kp=0.02, u0=0, e0=0):
    """PID Controller

    Arguments:
    y  .. Measured input of the System
    yc .. Desired Output of the System
    h  .. Sampling Time
    Kp .. Controller Gain Constant
    Ti .. Controller Integration Constant
    Td .. Controller Derivation Constant
    u0 .. Initial state of the integrator
    e0 .. Initial error

    Make sure this function gets called every h seconds!
    """

    # Step variable
    k = 0

    # Initialization
    ui_prev = u0
    e_prev = e0

    while 1:

            # Error between the desired and actual output
            y = y  + 20.00
            if y <  0.00:
                Y = 0.00
                
            yc = yc + 20.00
            if yc < 0.00:
                yc = 0.00
            e = yc - y

            # Integration Input
            ui = ui_prev + 1.00/Ti * h * e
            global integral
            integral = ui
            if ui < 2:
                ui=2
            if ui>12:
                ui=12

            
            # Derivation Input
            ud = 1.000/Td * (e - e_prev)/h
            global derivitive
            derivitive = ud 

            # Adjust previous values
            e_prev = e
            ui_prev = ui

            # Calculate output to the system
            u = Kp * (e + ui + ud)
            global output
            output = u
            # u1 = u
            #u = 12 - u
            if u < 2:
                u=2
            if u>12:
                u=12
                
            
            k += 1

            yield u

#------------------------------------------------------------------------------------------------------------
		# Get data from MPU 9250
'''
while True:

    t_interval = time.time()
    
    # if it's been longer than 5 seconds since last print
    if (t_interval - t_damp) > 5.0:

        if (t_interval - t_fail) > 1.0:
            t_one = 0
            t_three = 0
            roll_total = 0.0
            roll_run = [0] * 10
            heading_cos_total = 0.0
            heading_sin_total = 0.0
            heading_cos_run = [0] * 30
            heading_sin_run = [0] * 30
            t_fail_timer += 1
            print("MPU9250 not responding", "t_fail = ", t_fail, "t_shutdown = ", t_shutdown, "t_damp = ", t_damp)
            t_fail = t_interval
            t_shutdown += 1
            # retry sequence
            '''if(t_shutdown > 10):
                imu.setSlerpPower(0.02)
                imu.setGyroEnable(True)
                imu.setAccelEnable(True)
                imu.setCompassEnable(True)
                print("Resetting MPU comms")
                t_damp = 0
                t_fail_timer = 0
                t_shutdown = 0
            '''    
            
    
    # if IMU can be read then put info into data variable
    if imu.IMURead():
        data = imu.getIMUData()
        fusionPose = data["fusionPose"]
        Gyro = data["gyro"]
        t_fail_timer = 0.0

        if (t_interval - t_damp) > .1:
            roll = round(math.degrees(fusionPose[0]) - rolloff, 1)
            pitch = round(math.degrees(fusionPose[1]) - pitchoff, 1)
            yaw = round(math.degrees(fusionPose[2])- yawoff, 1)
            rollrate = round(math.degrees(Gyro[0]), 1)
            pitchrate = round(math.degrees(Gyro[1]), 1)
            yawrate = round(math.degrees(Gyro[2]), 1)
            if yaw < 0.1:
                yaw = yaw + 360
            if yaw > 360:
                yaw = yaw - 360

            # Dampening functions
            roll_total = roll_total - roll_run[t_one]
            roll_run[t_one] = roll
            roll_total = roll_total + roll_run[t_one]
            roll = round(roll_total / 10, 1)
            heading_cos_total = heading_cos_total - heading_cos_run[t_three]
            heading_sin_total = heading_sin_total - heading_sin_run[t_three]
            heading_cos_run[t_three] = math.cos(math.radians(yaw))
            heading_sin_run[t_three] = math.sin(math.radians(yaw))
            heading_cos_total = heading_cos_total + heading_cos_run[t_three]
            heading_sin_total = heading_sin_total + heading_sin_run[t_three]
            yaw = round(math.degrees(math.atan2(heading_sin_total/30,heading_cos_total/30)),1)
            if yaw < 0.1:
                yaw = yaw + 360.0

            # yaw is magnetic heading, convert to true heading
            heading = yaw - magnetic_deviation
            if heading < 0.1:
                heading = heading + 360
            if heading > 360:
                heading = heading - 360

            t_damp = t_interval
            t_one += 1
            if t_one == 10:
                t_one = 0
            t_three += 1
            if t_three == 30:
                t_three = 0

            if (t_interval - t_print) > 1:

             
                # print to console
                PID(5,2,1)
                x1 = PID()
                x1 = float(x1)
                print("Heading = ",heading ," - Roll = ", roll, " - Pitch = ", pitch, "  - Pitch SP = ", pitch_sp)
                print("PID values, Integral = ", integral," - Derivitive = ", derivitive, " - Output = ", output, "  - Pitch scaled SP", pitch_sp1)
                # Run PID loop to position Y Servo
                #pid_controller(pitch, pitch_sp)
                                
                # pid_controller(6, 8)
                # x1=(next(pid_controller(pitch, pitch_sp)))
                print (x1,  "  ",  u1)
                pwm.ChangeDutyCycle(x1)
                # to imu bus
                f = open('tracker_error_log', 'w')
                f.write(str(t_print) + ',' + str(heading) + ',' + str(roll)  + ',' + str(pitch))
                f.close()

              
                t_print = t_interval

        

        time.sleep(poll_interval*1.0/1000.0)
        
'''
        #---------------------------------------------------------------
        #
        # Servo Motor "Y" axis control

        # from tkinter import *
        # import RPi.GPIO as GPIO
        # import time

        # where 40 is the Y travel degrees vs full range (12)less zero position (2)
        # for the servo duty cycle frequency

        pitch_sp1 =  pitch / 4.0 + 7.0

        x = x + 1
        
        if x == 100:
            
            print(x)
            x = 0
            if (pitch - pitch_sp) < (pitch_hysterysis):
              # pwm.start(10)
              pwm.ChangeDutyCycle(pitch_sp1)
              print(" moving antenna back")
              # pwm.start(0)
            if (pitch - pitch_sp) > (pitch_hysterysis):
              # pwm.start(10)
              pwm.ChangeDutyCycle(pitch_sp1)
              print("Moving antenna ahead")
              # pwm.start(0)
           
            
  
  
'''
'''

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=0, to=180,
              orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)


    def update(self, angle):
        duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)

root = Tk()
root.wm_title("Ricks Wifi AP Antenna Tracker")
    servo = Tk()
    servo.wm_title('Servo Control')
    app = App(servo)
    servo.geometry("300x75+0+0")
    
root.geometry("400x500+0+0")
root.mainloop()
'''


        

        
