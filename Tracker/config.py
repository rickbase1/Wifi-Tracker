# global variables config

# stepper_status = False  # used for ensuring thread only runs sequenitally
import Tracker
import compass
#import gui

  # compass global variables   
heading = 0.0       
pitch = 0.0         
tilt = 0.0   

  # stepper global variables
stepper_error = 0.0
stepper_error1 = 0.0
stepper_direction = 0.0
stepper_hysterysis = 0.0
speed = 0.0
stepper_direction = "null"

#import gui
# gui setpoints

heading_sp = 0.0
pitch_sp = 0.0

# Tracker variables
heading_sp = 257.0  # compass heading setpoint ( geo info added laterng
heading = 0.0       
pitch = 0.0         
tilt = 0.0   

t_interval = 0.0
t_print = 0.0


# Servo PID parameters
Servo_P_gain = 0.24 # 0.27
Servo_I_gain = 0.45  # 0.19
Servo_D_gain = 0.002  # 0.01
Servo_I_windup = 0.1  # 3.5
Servo_Bias = 13.25  # 13.75
Servo_Min = 5.0  # 5.0
Servo_Max = 17.0 # 17.0
# -------------------------- Calculated Variables ------------
Servo_Derivator = 0.0
Servo_Integrator = 0.0
Servo_t_pid =0.0
Servo_t_PID = 0.75
Servo_pitch_sp = 4.0
Servo_output = 0.0
    
  

#_thread.start_new_thread (compass.compass_data())
from threading import Thread
import _thread

t1 = Thread(target = compass.compass_data)

#t2 = Thread(target = Tracker.run_servo_stepper)  #(Servo_P_gain, Servo_I_gain, Servo_D_gain, Servo_I_windup, Servo_Bias, Servo_Min, Servo_Max))
#t2 = Thread(target =gui.py)

t1.start()
print("config Thread 1, compass started")
#t2.start()
#print("config Thread 2, Tracker started.  Total active threads is , threading.active_count()")
 
#compass.compass_data()

# from stepper.py


# from servo.py




