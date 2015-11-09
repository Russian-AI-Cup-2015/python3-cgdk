from math import *
from model.Unit import Unit


class CircularUnit(Unit):
    def __init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, radius):
        Unit.__init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed)

        self.radius = radius