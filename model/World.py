from math import *
from model.Bonus import Bonus
from model.Car import Car
from model.Direction import Direction
from model.OilSlick import OilSlick
from model.Player import Player
from model.Projectile import Projectile
from model.TileType import TileType


class World:
    def __init__(self, tick, tick_count, last_tick_index, width, height, players, cars, projectiles, bonuses,
                 oil_slicks, map_name, tiles_x_y, waypoints, starting_direction: (None, Direction)):
        self.tick = tick
        self.tick_count = tick_count
        self.last_tick_index = last_tick_index
        self.width = width
        self.height = height
        self.players = players
        self.cars = cars
        self.projectiles = projectiles
        self.bonuses = bonuses
        self.oil_slicks = oil_slicks
        self.map_name = map_name
        self.tiles_x_y = tiles_x_y
        self.waypoints = waypoints
        self.starting_direction = starting_direction

    def get_my_player(self):
        for player in self.players:
            if player.me:
                return player

        return None