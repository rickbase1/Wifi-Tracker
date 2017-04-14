#!/usr/bin/python3

import time

class PID:
    """PID Controller
    """

    def __init__(self, P, I, D, Min, Max):

        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.min_range = Min
        self.max_range = Max

        self.sample_time = 1.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 12.5
        self.windup_guard = 5.0

        self.output = 0.0
        #error = 0.0
        print("Variables cleared from PID Loop")

    def update(self, input):
              
        error = self.SetPoint - input

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)+ self.int_error
            if (self.output > self.max_range):
                self.output = self.max_range
                
            if (self.output < self.min_range):
                self.output = self.min_range
            
            # loop verification
            
            #print("PID_SP = ", self.SetPoint, "Input = ", input,  "Output = ", self.output, "PID", self.Kp, self.Ki, self.Kd)
            print ("PID Error ", error, "Delta Error ", delta_error, "Self Windup Guard", self.windup_guard, "Pgain ", self.Kp, "Igain", self.Ki, "Int/time ", self.ITerm, "Dgain ", self.Kd)
    
    def PGain(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def IGain(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def DGain(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def IGWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def SampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time
