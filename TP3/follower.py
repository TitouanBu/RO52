from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, ColorSensor , UltrasonicSensor
from pybricks.tools import wait
from log import write_log,clear_log

class Follower:
    def __init__(self, left_motor_port, right_motor_port, color_sensor_port,sonic_sensor_port,
                limit, wheel_diameter = 55.5, axle_track = 104, tau = 0.1, max_angle = 100):
        
        self.max_angle = max_angle
        self.tau  = tau
        self.old_error = 0
        self.error_history = 0
        self.is_white = True
        self.limit = limit
        self.sonicsensor = UltrasonicSensor(sonic_sensor_port)
        self.drivebase = DriveBase(Motor(left_motor_port), Motor(right_motor_port), wheel_diameter, axle_track)
        self.sensor = ColorSensor(color_sensor_port)
        self.speed = int(250)
        self.previous_coeff = 0.5


    def tout_ou_rien(self, k_p, k_i, k_d):
        while True:
            if self.sonicsensor.distance() < 150 :
                self.speed = 0
                # wait(500)
            # Cas noir :
            if self.sensor.reflection() < self.limit:
                if self.is_white:
                    self._clean()
                else:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                self.drivebase.drive(self.speed, - self._angle(k_p, k_i, k_d))
            # Cas blanc :
            else:
                if self.is_white:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                else:
                    self._clean()
                self.drivebase.drive(self.speed, self._angle(k_p, k_i, k_d))
            wait(self.tau * 1000)
            write_log(self.sonicsensor.distance(),self.speed)

    def a_un_point(self, k_p, k_i, k_d, distance, coeff_a):
        while True:
            #calcul speed
            # D = 150 / d(t) => distance
            D = distance
            a = coeff_a
            diff = self.sonicsensor.distance() - D
            coef = max(min(50, a*(diff)),0)
            self.speed = int(250*(coef/100))
            # Cas noir :
            if self.sensor.reflection() < self.limit:
                if self.is_white:
                    self._clean()
                else:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                self.drivebase.drive(self.speed, - self._angle(k_p, k_i, k_d))
            # Cas blanc :
            else:
                if self.is_white:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                else:
                    self._clean()
                self.drivebase.drive(self.speed, self._angle(k_p, k_i, k_d))
            wait(self.tau * 1000)
            write_log(self.sonicsensor.distance(),self.speed)

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
            self.speed = int(250*min(coef_f,coef_a)/100)
            self.previous_coeff = coef_a
            if self.sonicsensor.distance() < 150 :
                self.speed = 0
                # wait(500)
            # Cas noir :
            if self.sensor.reflection() < self.limit:
                if self.is_white:
                    self._clean()
                else:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                self.drivebase.drive(self.speed, - self._angle(k_p, k_i, k_d))
            # Cas blanc :
            else:
                if self.is_white:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                else:
                    self._clean()
                self.drivebase.drive(self.speed, self._angle(k_p, k_i, k_d))
            wait(self.tau * 1000)
            write_log(self.sonicsensor.distance(),self.speed)

    def _current_err(self):
        return abs(self.sensor.reflection() - self.limit)

    def _angle(self, k_p: float, k_i: float, k_d: float):
        result = (k_p * self._current_err())+ (k_i * self.tau) * self.error_history + (k_d/self.tau)*(self.error_history-self.old_error)
        return result if result < self.max_angle else self.max_angle
    
    def _clean(self):
        self.error_history = 0
        self.old_error = 0
        self.is_white = not self.is_white