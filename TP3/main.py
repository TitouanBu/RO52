#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from leader import Leader
from follower import Follower
from log import clear_log

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
clear_log()
ev3 = EV3Brick()
############################### LEADER

# au démarrage :
server = BluetoothMailboxServer
channel = TextMailbox("speed",server)
try:
    server.wait_for_connection()
except:
    # tout ou rien
    pass



# à integrer dans le cycle loop :
try:
    channel.send("speed")
except:
    # tout ou rien
    pass
# leader1 = Leader(Port.A,Port.B,Port.S3,50,max_angle=100)
# leader1.follow_line(0.5, 0.5, 0.05, 5000)

############################### FOLLOWER

#################### TOUT OU RIEN
# follower1 = Follower(Port.A,Port.B,Port.S3,Port.S1,50,max_angle=100)
# follower1.tout_ou_rien(0.5, 0.5, 0.05)

#################### A UN POINT
# follower1 = Follower(Port.A,Port.B,Port.S3,Port.S1,50,max_angle=100)
# follower1.a_un_point(0.5, 0.5, 0.05,200,0.1)

# Valeurs de test A un point
# #1 : 0.5, 0.5, 0.05, 100, 0.1
# #2 : 0.5, 0.5, 0.05, 100, 0.5
# #3 : 0.5, 0.5, 0.05, 100, 0.7
# #4 : 0.5, 0.5, 0.05, 200, 0.5
# #5 : 0.5, 0.5, 0.05, 200, 0.1

#################### A DEUX POINT
follower1 = Follower(Port.A,Port.B,Port.S3,Port.S1,50,max_angle=100)
follower1.a_deux_point(0.5, 0.5, 0.05, 0.3, 0.3, 100, 200)

# Valeurs de test A deux points
# #1 : 0.5, 0.5, 0.05, 0.2, 0.2, 100, 300
# #2 : 0.5, 0.5, 0.05, 0.2, 0.5, 100, 300
# #3 : 0.5, 0.5, 0.05, 0.5, 0.5, 100, 300
# #4 : 0.5, 0.5, 0.05, 0.3, 0.3, 100, 300
# #5 : 0.5, 0.5, 0.05, 0.3, 0.3, 100, 200

# Valeurs de test A deux points VITESSE ERRONEE
# #1 : 0.5, 0.5, 0.05, 0.5, 0.5, 100, 300
# #2 : 0.5, 0.5, 0.05, 0.7, 0.3, 100, 300
# #3 : 0.5, 0.5, 0.05, 0.3, 0.7, 100, 300
# #4 : 0.5, 0.5, 0.05, 0.5, 2, 100, 300
# #5 : 0.5, 0.5, 0.05, 2, 0.7, 100, 300

#Valeurs pour différents parcours
#0.5, 0.5, 0.05, 150 => Parcours en 8
#0.2, 0 , 0.1 , 250 => ligne droite
#0.5, 0.5, 0.1 , 150 => courbe