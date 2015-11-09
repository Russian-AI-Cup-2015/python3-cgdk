from math import *
from model.CarType import CarType
from model.RectangularUnit import RectangularUnit


class Car(RectangularUnit):
    def __init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, width, height, player_id, teammate_index,
                 teammate, type: (None, CarType), projectile_count, nitro_charge_count, oil_canister_count,
                 remaining_projectile_cooldown_ticks, remaining_nitro_cooldown_ticks, remaining_oil_cooldown_ticks,
                 remaining_nitro_ticks, remaining_oiled_ticks, durability, engine_power, wheel_turn, next_waypoint_x,
                 next_waypoint_y, finished_track):
        RectangularUnit.__init__(self, id, mass, x, y, speed_x, speed_y, angle, angular_speed, width, height)

        self.player_id = player_id
        self.teammate_index = teammate_index
        self.teammate = teammate
        self.type = type
        self.projectile_count = projectile_count
        self.nitro_charge_count = nitro_charge_count
        self.oil_canister_count = oil_canister_count
        self.remaining_projectile_cooldown_ticks = remaining_projectile_cooldown_ticks
        self.remaining_nitro_cooldown_ticks = remaining_nitro_cooldown_ticks
        self.remaining_oil_cooldown_ticks = remaining_oil_cooldown_ticks
        self.remaining_nitro_ticks = remaining_nitro_ticks
        self.remaining_oiled_ticks = remaining_oiled_ticks
        self.durability = durability
        self.engine_power = engine_power
        self.wheel_turn = wheel_turn
        self.next_waypoint_x = next_waypoint_x
        self.next_waypoint_y = next_waypoint_y
        self.finished_track = finished_track