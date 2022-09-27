#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

import struct

# This program uses the two PS4 sticks to control two EV3 Large Servo Motors using tank like controls

# Create your objects here.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
medium_motor = Motor(Port.D)
large_motor = Motor(Port.A)
left_speed = 0
right_speed = 0
medium_motor_speed = 0
large_motor_speed =  0

# Locat the event file you want to react to, on my setup the PS4 controller button events
# are located in /dev/input/event4
infile_path = "/dev/input/event4"
in_file = open(infile_path, "rb")

# Define the format the event data will be read
# See https://docs.python.org/3/library/struct.html#format-characters for more details
FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)

# A helper function for converting stick values (0 to 255) to more usable numbers (-100 to 100)
def scale(val, src, dst):
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

# Create a loop to react to events
while event:

    # Place event data into variables
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

    if ev_type == 3: # Stick was moved

        # React to the left stick
        if code == 1:
            left_speed = scale(value, (0,255), (100, -100))
        
        # React to the right stick
        if code == 4:
            right_speed = scale(value, (0,255), (100, -100))


    # If a button was pressed or released
    elif ev_type == 1:

        # React to the L1 button. Medium Motor Buttons
        if code == 310 and value == 0:
            print("The L1 button was released")
            medium_motor_speed = value*-100
        elif code == 310 and value == 1:
            print("The L1 button was pressed")
            medium_motor_speed = value*-100

        # React to the L2 button
        elif code == 312 and value == 0:
            print("The L2 button was released")
            medium_motor_speed = value*100
        elif code == 312 and value == 1:
            print("The L2 button was pressed")
            medium_motor_speed = value*100

        # React to the R1 button. Large Motor Buttons
        elif code == 311 and value == 0:
            print("The R1 button was released")
            large_motor_speed = value*-100
        elif code == 311 and value == 1:
            print("The R1 button was pressed")
            large_motor_speed = value*-100

        # React to the R2 button
        elif code == 313 and value == 0:
            print("The R2 button was released")
            large_motor_speed = value*100
        elif code == 313 and value == 1:
            print("The R2 button was pressed")
            large_motor_speed = value*100

    
    
    # Set motor speed
    left_motor.dc(left_speed)
    right_motor.dc(right_speed)
    medium_motor.dc(medium_motor_speed)
    large_motor.dc(large_motor_speed)

    # Read the next event
    event = in_file.read(EVENT_SIZE)

in_file.close()