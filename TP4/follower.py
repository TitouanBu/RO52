from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, ColorSensor , UltrasonicSensor, GyroSensor
from pybricks.tools import wait,DataLog, StopWatch
from math import cos, sin, radians

isNegatif = None

class Follower:
    def __init__(self, left_motor_port, right_motor_port, color_sensor_port,sonic_sensor_port, gyro_sensor_port,
                limit, wheel_diameter = 55.5, axle_track = 104, tau = 0.1, max_angle = 100):
        self.max_angle = max_angle
        self.tau  = tau
        self.old_error = 0
        self.error_history = 0
        self.is_white = True
        self.limit = limit
        self.sonicsensor = UltrasonicSensor(sonic_sensor_port)
        self.drivebase = DriveBase(Motor(left_motor_port), Motor(right_motor_port), wheel_diameter, axle_track)
        self.gyrosensor = GyroSensor(gyro_sensor_port)
        self.log_file = DataLog("distance","drive speed","angle","turn rate","x","y",name="log",timestamp=False,append=False)
        self.sensor = ColorSensor(color_sensor_port)
        self.speed = int(250)
        self.previous_coeff = 0.5
        self.x = 0
        self.y = 0
        self.angle = 0
        self.distance = 0
        self.observed_speed = 0
        self.turn_rate = 0
        self.timer = StopWatch()
        self.gyrosensor.reset_angle(0)

        #initialisation khalman
        self.angle_kalman = 0
        self.gyro_angle = 0
        self.variation = 0.5 # variable  à définir => variation maximum

    def a_deux_point(self, k_p, k_i, k_d, coeff_f, coeff_a, distance_f, distance_a):
        while True:
            #calcule vitesse freinage
            a_f = coeff_f
            D_f = distance_f
            diff_f = self.sonicsensor.distance() - D_f
            coef_f = min(max(a_f*diff_f,0),50)

            #calcule vitesse acceleration 
            a_a = coeff_a
            D_a = distance_a
            diff_a = self.sonicsensor.distance() - D_a
            coef_a = min(max(a_a*diff_a,0,self.previous_coeff),50)

            #calcule vitesse finale 
            self.speed = int(250*(min(coef_f,coef_a)/100))
            self.previous_coeff = coef_a
            if self.sonicsensor.distance() < 150 :
                self.speed = 0
                # wait(500)

            # Timer 
            self.timer.reset()
            self.timer.resume()

            # Cas noir :
            if self.sensor.reflection() < self.limit:
                if self.is_white:
                    self._clean()
                else:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                self.drivebase.drive(self.speed, - self._angle(k_p, k_i, k_d))
                self.turn_rate = - self._angle(k_p, k_i, k_d)
                self.kalman(- self._angle(k_p, k_i, k_d))
            # Cas blanc :
            else:
                if self.is_white:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                else:
                    self._clean()
                self.drivebase.drive(self.speed, self._angle(k_p, k_i, k_d))
                self.turn_rate = self._angle(k_p, k_i, k_d)
                self.kalman(self._angle(k_p, k_i, k_d))
                
            wait(self.tau * 1000)
            # self.actualize_position_drivebase()
            # self.actualize_position_gyro()
            # self.actualize_position_drive(self.turn_rate)

    def actualize_position_drive(self,drive_angle):
        old_angle = self.angle
        self.angle = drive_angle*(self.timer.time()/1000)
        #old_distance = self.distance
        self.distance = (self.speed*(self.timer.time()))/1000
            
        self.x = self.x + (self.distance)*cos((self.angle+old_angle)/2)
        self.y = self.y + (self.distance)*sin((self.angle+old_angle)/2)
        self.log_file.log(self.distance,self.observed_speed,self.angle,self.timer.time(),self.x,self.y)

    def actualize_position_drivebase(self):
        state = self.drivebase.state()
        old_angle = self.angle
        # self.angle = radians(state[2])
        self.angle = self.angle_kalman
        old_distance = self.distance
        self.distance = state[0]
        old_observed_speed = self.observed_speed
        self.observed_speed = state[1]
        """old_turn_rate = self.turn_rate
        self.turn_rate = state[3]"""
            
        self.x = self.x + (self.distance-old_distance)*cos((self.angle+old_angle)/2)
        self.y = self.y + (self.distance-old_distance)*sin((self.angle+old_angle)/2)
        self.log_file.log(self.distance,self.observed_speed,self.angle,self.turn_rate,self.x,self.y)

    def actualize_position_gyro(self):
        old_angle = self.angle
        angle = self.gyrosensor.angle()
        self.angle = radians(angle)
        #old_distance = self.distance
        self.distance = (self.speed*(self.timer.time()))/1000
            
        self.x = self.x + (self.distance)*cos((self.angle+old_angle)/2)
        self.y = self.y + (self.distance)*sin((self.angle+old_angle)/2)
        self.log_file.log(self.distance,self.observed_speed,angle,self.timer.time(),self.x,self.y)
        self.gyrosensor.reset_angle(angle)


    def kalman(self,speed_angle):
        #calcul angle theoriqe
        estimation_angle = self.angle_kalman + (self.timer.time()/1000)*speed_angle + radians(10) # constante à définir
       
        #calcul de l'angle réel
        gyro_angle = self.gyrosensor.angle()
        self.gyro_angle = radians(gyro_angle)

        #estimation erreur et correction
        K = self.variation / (self.variation + radians(10)) # 10°  ou 30°
        error = self.gyro_angle - estimation_angle
        self.angle_kalman = estimation_angle + K*error

        self.variation = (1-K)*self.variation
        #self.gyrosensor.reset_angle(angle)
        """
        #penser à initialiser 
        angle = 0 
        previous_angle = 0
        variation = 0.5  # à définir

        #calcul angle theorique

        estimation_angle = angle + time*speed_angle + radian(10) #calcul du nouveau angle

        #calcul angle veridique
        
        K = variation / (variation + radian(10)) # 10°  ou 30°
        error = angle_gyro - estimation_angle
        angle = estimation_angle + K*error

        variation = (1-K)*variation
        """

    def _current_err(self):
        return abs(self.sensor.reflection() - self.limit)

    def _angle(self, k_p: float, k_i: float, k_d: float):
        result = (k_p * self._current_err())+ (k_i * self.tau) * self.error_history + (k_d/self.tau)*(self.error_history-self.old_error)
        return result if result < self.max_angle else self.max_angle
    
    def _clean(self):
        self.error_history = 0
        self.old_error = 0
        self.is_white = not self.is_white
