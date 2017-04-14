

import sys

sys.path.append('.')
import RTIMU
import os.path
import time
import math
#import socket
import os
#import pickle
#import json
import servo
import PID

import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#DEBUG = False


# discover IMU

SETTINGS_FILE = "RTIMULib" # all parameters and calibration data is stored here

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
logging.debug (s)
logging.debug (imu)

#print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  logging.debug("Settings file does not exist, will be created")
else:
   logging.debug("Settings File " + SETTINGS_FILE + " found")
   
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
    logging.debug("MPU9250 IMU magnemometer failed to initialize on i2c bus")
    sys.exit(1)
else:
    print("MPU9250 IMU Init Succeeded");

    
# configure IMU parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
logging.debug("Poll interval retreived and set to ", poll_interval, " milliseconds")

if imu.getCompassCalibrationEllipsoidValid():
    logging.debug("Compass is using Ellipsoid data")

if imu.getCompassCalibrationValid():
    logging.debug("compass is using min/max data")


# initialize data variables

roll = 0.0
pitch = 0.0
yaw = 0.0
heading = 0.0
rollrate = 0.0
pitchrate = 0.0
yawrate = 0.0



# magnetic deviation
# use file "mag" in current directory to set offset
# todo, get offset based on geolocate data from nooa tables

f = open('mag', 'r')
magnetic_deviation = float(f.readline())
logging.debug("Magnetic Deviation is ", magnetic_deviation)
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

# Servo PID config

pid = PID.PID(P=0.5,I=0.1,D=0)
servo_PID_out = pid.output

#------------------------------------------------------------------------------------------------------------
		# Get data from MPU 9250

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
            logging.debug("MPU9250 not responding", "t_fail = ", t_fail, "t_shutdown = ", t_shutdown, "t_damp = ", t_damp)
            t_fail = t_interval
            t_shutdown += 1
                      
    
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
            
            if (t_interval - t_print) > 0.5:

               # print to console
               
                print("Heading = ",heading ," - Roll = ", roll, " - Pitch = ", pitch)
                                
               # print to file, TODO, set up error reporting, not just variables
                '''
                f = open('tracker_error_log', 'w')
                f.write(str(t_print) + ',' + str(heading) + ',' + str(roll)  + ',' + str(pitch))
                f.close()
                '''
                t_print = t_interval
                
        # if __name__ == "__main__":   

        #compass_data = (heading, yaw, pitch)
            servo.SERVO.SetPosition(pitch)
        #pickle.dump(compass_data, open( "compass_data.p", "wb"))
        # os.environ["COMPASS_DATA"] = json.dumps(compass_data)
        # print("scanned")    

#--------------------------------------------
        # PID Control

        #pid(0.8, 0.5, 0.001)
        
        # print (servo_PID_out)

    time.sleep(poll_interval*1.0/1000.0)
        


        

        
