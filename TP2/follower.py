from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.tools import wait
from logCSV import write_log,clear_log

class Follower:
    def __init__(self, left_motor_port, right_motor_port, color_sensor_port,
                limit, wheel_diameter = 55.5, axle_track = 104, tau = 0.1, max_angle = 100):
        
        self.max_angle = max_angle
        self.tau  = tau
        self.old_error = 0
        self.error_history = 0
        self.is_white = True
        self.limit = limit
        self.drivebase = DriveBase(Motor(left_motor_port), Motor(right_motor_port), wheel_diameter, axle_track)
        self.sensor = ColorSensor(color_sensor_port)


    def follow_line(self, k_p, k_i, k_d, speed = 50):
        while True:
            # Cas noir :
            if self.sensor.reflection() < self.limit:
                if self.is_white:
                    self._clean()
                else:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                self.drivebase.drive(speed, - self._angle(k_p, k_i, k_d))
            # Cas blanc :
            else:
                if self.is_white:
                    self.old_error = self.error_history
                    self.error_history += self._current_err()
                else:
                    self._clean()
                self.drivebase.drive(speed, self._angle(k_p, k_i, k_d))
            wait(self.tau * 1000)
            write_log(self.error_history)


    def _current_err(self):
        return abs(self.sensor.reflection() - self.limit)

    def _angle(self, k_p: float, k_i: float, k_d: float):
        result = (k_p * self._current_err())+ (k_i * self.tau) * self.error_history + (k_d/self.tau)*(self.error_history-self.old_error)
        return result if result < self.max_angle else self.max_angle
    
    def _clean(self):
        self.error_history = 0
        self.old_error = 0
        self.is_white = not self.is_white