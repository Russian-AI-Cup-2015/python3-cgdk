from math import *
from model.CircularUnit import CircularUnit
from model.ProjectileType import ProjectileType


class Projectile(CircularUnit):
    def __init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, radius, car_id, player_id,
                 type: (None, ProjectileType)):
        CircularUnit.__init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, radius)

        self.car_id = car_id
        self.player_id = player_id
        self.type = type