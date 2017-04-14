#!/usr/bin/python3
import PID
import time



pid=PID.PID(P=1.5, I=0.2, D=0.1, Min = 4.0, Max = 20.0)


pid.SetPoint=50.0
#pid.setSampleTime(0.1)

input = 0.0
output = 0.0
#pid.Igain = 0.1
#pid.Dgain = 0.01
#pid.IGWindup = 0.1
#x=0.0
#pid.clear()
time.sleep(5.0)
for x in range (1, 1000):
    
    input = x / 1
    pid.update(input)
    time.sleep(0.5)
    output = pid.output
    print ("Test_pgm setpoint, input and output)", pid.SetPoint, input, output)
    time.sleep(0.5)
        
    
    
