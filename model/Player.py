from math import *


class Player:
    def __init__(self, id, me, name, strategy_crashed, score):
        self.id = id
        self.me = me
        self.name = name
        self.strategy_crashed = strategy_crashed
        self.score = score