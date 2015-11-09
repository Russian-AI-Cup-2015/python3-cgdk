from math import *


class Move:
    def __init__(self):
        self.engine_power = 0.0
        self.brake = False
        self.wheel_turn = 0.0
        self.throw_projectile = False
        self.use_nitro = False
        self.spill_oil = False