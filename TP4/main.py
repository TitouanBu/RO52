#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from follower import Follower

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()
############################### LEADER

#################### A DEUX POINT
follower1 = Follower(Port.A,Port.B,Port.S3,Port.S1,Port.S2,50,max_angle=100)
follower1.a_deux_point(0.5, 0.5, 0.05, 0.3, 0.3, 100, 200)