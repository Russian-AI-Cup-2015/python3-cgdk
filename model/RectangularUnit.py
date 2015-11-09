from math import *
from model.Unit import Unit


class RectangularUnit(Unit):
    def __init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, width, height):
        Unit.__init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed)

        self.width = width
        self.height = height