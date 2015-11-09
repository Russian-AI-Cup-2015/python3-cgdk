from math import *
from model.BonusType import BonusType
from model.RectangularUnit import RectangularUnit


class Bonus(RectangularUnit):
    def __init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, width, height, type: (None, BonusType)):
        RectangularUnit.__init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, width, height)

        self.type = type