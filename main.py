#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from follower import Follower
from logCSV import clear_log

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
clear_log()
ev3 = EV3Brick()
follower1 = Follower(Port.A,Port.B,Port.S3,50,max_angle=100)
follower1.follow_line(0.7, 0, 0, 150)

#Valeurs pour différents parcours
#0.5, 0.5, 0.05, 150 => Parcours en 8
#0.2, 0 , 0.1 , 250 => ligne droite
#0.5, 0.5, 0.1 , 150 => courbe