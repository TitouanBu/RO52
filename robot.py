#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.robotics import DriveBase
from pybricks.parameters import Port

class Robot :
    def __init__(self):
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.B)

    def forward(self,speed):
        self.left_motor.run(speed)
        self.right_motor.run(speed)

    def rotate(self,angle,aSpeed):
        print(self.left_motor.angle())
        self.left_motor.run(-aSpeed)
        self.right_motor.run(aSpeed)
        #self.left_motor.run_angle(aSpeed,angle)
        #self.right_motor.run_angle(-aSpeed,angle)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()  

class Sensor :
    def __init__(self,mode:str):
        if(mode == "IR"):
            self.sensor = InfraredSensor(Port.S1)
        else:
            self.sensor = UltrasonicSensor(Port.S1)

    def distance(self):
        return self.sensor.distance()

class Color_Sensor :
    def __init__(self):
        self.sensor = ColorSensor(Port.s4)
    
    def color(self):
        return self.sensor.color()

class Status :
    def __init__(self):
        pass

    def update_distance(self,distance):
        self.distance = distance
    
    def update_couleur(self,couleur):
        self.couleur = couleur