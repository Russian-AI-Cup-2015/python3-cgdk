from math import *


class Game:
    def __init__(self, random_seed, tick_count, world_width, world_height, track_tile_size, track_tile_margin,
                 lap_count, lap_tick_count, initial_freeze_duration_ticks, burning_time_duration_factor,
                 finish_track_scores, finish_lap_score, lap_waypoints_summary_score_factor, car_damage_score_factor,
                 car_elimination_score, car_width, car_height, car_engine_power_change_per_tick,
                 car_wheel_turn_change_per_tick, car_angular_speed_factor, car_movement_air_friction_factor,
                 car_rotation_air_friction_factor, car_lengthwise_movement_friction_factor,
                 car_crosswise_movement_friction_factor, car_rotation_friction_factor, throw_projectile_cooldown_ticks,
                 use_nitro_cooldown_ticks, spill_oil_cooldown_ticks, nitro_engine_power_factor, nitro_duration_ticks,
                 car_reactivation_time_ticks, buggy_mass, buggy_engine_forward_power, buggy_engine_rear_power,
                 jeep_mass, jeep_engine_forward_power, jeep_engine_rear_power, bonus_size, bonus_mass,
                 pure_score_amount, washer_radius, washer_mass, washer_initial_speed, washer_damage, side_washer_angle,
                 tire_radius, tire_mass, tire_initial_speed, tire_damage_factor, tire_disappear_speed_factor,
                 oil_slick_initial_range, oil_slick_radius, oil_slick_lifetime, max_oiled_state_duration_ticks):
        self.random_seed = random_seed
        self.tick_count = tick_count
        self.world_width = world_width
        self.world_height = world_height
        self.track_tile_size = track_tile_size
        self.track_tile_margin = track_tile_margin
        self.lap_count = lap_count
        self.lap_tick_count = lap_tick_count
        self.initial_freeze_duration_ticks = initial_freeze_duration_ticks
        self.burning_time_duration_factor = burning_time_duration_factor
        self.finish_track_scores = finish_track_scores
        self.finish_lap_score = finish_lap_score
        self.lap_waypoints_summary_score_factor = lap_waypoints_summary_score_factor
        self.car_damage_score_factor = car_damage_score_factor
        self.car_elimination_score = car_elimination_score
        self.car_width = car_width
        self.car_height = car_height
        self.car_engine_power_change_per_tick = car_engine_power_change_per_tick
        self.car_wheel_turn_change_per_tick = car_wheel_turn_change_per_tick
        self.car_angular_speed_factor = car_angular_speed_factor
        self.car_movement_air_friction_factor = car_movement_air_friction_factor
        self.car_rotation_air_friction_factor = car_rotation_air_friction_factor
        self.car_lengthwise_movement_friction_factor = car_lengthwise_movement_friction_factor
        self.car_crosswise_movement_friction_factor = car_crosswise_movement_friction_factor
        self.car_rotation_friction_factor = car_rotation_friction_factor
        self.throw_projectile_cooldown_ticks = throw_projectile_cooldown_ticks
        self.use_nitro_cooldown_ticks = use_nitro_cooldown_ticks
        self.spill_oil_cooldown_ticks = spill_oil_cooldown_ticks
        self.nitro_engine_power_factor = nitro_engine_power_factor
        self.nitro_duration_ticks = nitro_duration_ticks
        self.car_reactivation_time_ticks = car_reactivation_time_ticks
        self.buggy_mass = buggy_mass
        self.buggy_engine_forward_power = buggy_engine_forward_power
        self.buggy_engine_rear_power = buggy_engine_rear_power
        self.jeep_mass = jeep_mass
        self.jeep_engine_forward_power = jeep_engine_forward_power
        self.jeep_engine_rear_power = jeep_engine_rear_power
        self.bonus_size = bonus_size
        self.bonus_mass = bonus_mass
        self.pure_score_amount = pure_score_amount
        self.washer_radius = washer_radius
        self.washer_mass = washer_mass
        self.washer_initial_speed = washer_initial_speed
        self.washer_damage = washer_damage
        self.side_washer_angle = side_washer_angle
        self.tire_radius = tire_radius
        self.tire_mass = tire_mass
        self.tire_initial_speed = tire_initial_speed
        self.tire_damage_factor = tire_damage_factor
        self.tire_disappear_speed_factor = tire_disappear_speed_factor
        self.oil_slick_initial_range = oil_slick_initial_range
        self.oil_slick_radius = oil_slick_radius
        self.oil_slick_lifetime = oil_slick_lifetime
        self.max_oiled_state_duration_ticks = max_oiled_state_duration_ticks