from math import *
from model.CircularUnit import CircularUnit


class OilSlick(CircularUnit):
    def __init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, radius, remaining_lifetime):
        CircularUnit.__init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, radius)

        self.remaining_lifetime = remaining_lifetime