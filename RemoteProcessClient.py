import _socket
import struct

from model.Car import Car
from model.CarType import CarType
from model.Direction import Direction
from model.Projectile import Projectile
from model.ProjectileType import ProjectileType
from model.TileType import TileType
from model.Bonus import Bonus
from model.BonusType import BonusType
from model.Game import Game
from model.Move import Move
from model.OilSlick import OilSlick
from model.Player import Player
from model.PlayerContext import PlayerContext
from model.World import World


class RemoteProcessClient:
    LITTLE_ENDIAN_BYTE_ORDER = True

    BYTE_ORDER_FORMAT_STRING = "<" if LITTLE_ENDIAN_BYTE_ORDER else ">"

    SIGNED_BYTE_SIZE_BYTES = 1
    INTEGER_SIZE_BYTES = 4
    LONG_SIZE_BYTES = 8
    DOUBLE_SIZE_BYTES = 8

    def __init__(self, host, port):
        self.socket = _socket.socket()
        self.socket.setsockopt(_socket.IPPROTO_TCP, _socket.TCP_NODELAY, True)
        self.socket.connect((host, port))
        self.map_name = None
        self.tiles_x_y = None
        self.waypoints = None
        self.starting_direction = None

    def write_token_message(self, token):
        self.write_enum(RemoteProcessClient.MessageType.AUTHENTICATION_TOKEN)
        self.write_string(token)

    def read_team_size_message(self):
        message_type = self.read_enum(RemoteProcessClient.MessageType)
        self.ensure_message_type(message_type, RemoteProcessClient.MessageType.TEAM_SIZE)
        return self.read_int()

    def write_protocol_version_message(self):
        self.write_enum(RemoteProcessClient.MessageType.PROTOCOL_VERSION)
        self.write_int(1)

    def read_game_context_message(self):
        message_type = self.read_enum(RemoteProcessClient.MessageType)
        self.ensure_message_type(message_type, RemoteProcessClient.MessageType.GAME_CONTEXT)
        return self.read_game()

    def read_player_context_message(self):
        message_type = self.read_enum(RemoteProcessClient.MessageType)
        if message_type == RemoteProcessClient.MessageType.GAME_OVER:
            return None

        self.ensure_message_type(message_type, RemoteProcessClient.MessageType.PLAYER_CONTEXT)
        return self.read_player_context()

    def write_moves_message(self, moves):
        self.write_enum(RemoteProcessClient.MessageType.MOVE)
        self.write_moves(moves)

    def close(self):
        self.socket.close()

    def read_bonus(self):
        if not self.read_boolean():
            return None

        return Bonus(
            self.read_long(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_enum(BonusType)
        )

    def write_bonus(self, bonus):
        if bonus is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_long(bonus.id)
            self.write_double(bonus.mass)
            self.write_double(bonus.x)
            self.write_double(bonus.y)
            self.write_double(bonus.speed_x)
            self.write_double(bonus.speed_y)
            self.write_double(bonus.angle)
            self.write_double(bonus.angular_speed)
            self.write_double(bonus.width)
            self.write_double(bonus.height)
            self.write_enum(bonus.type)

    def read_bonuses(self):
        bonus_count = self.read_int()
        if bonus_count < 0:
            return None

        bonuses = []

        for _ in range(bonus_count):
            bonuses.append(self.read_bonus())

        return bonuses

    def write_bonuses(self, bonuses):
        if bonuses is None:
            self.write_int(-1)
        else:
            self.write_int(bonuses.__len__())

            for bonus in bonuses:
                self.write_bonus(bonus)

    def read_car(self):
        if not self.read_boolean():
            return None

        return Car(
            self.read_long(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_long(), self.read_int(), self.read_boolean(), self.read_enum(CarType), self.read_int(),
            self.read_int(), self.read_int(), self.read_int(), self.read_int(), self.read_int(), self.read_int(),
            self.read_int(), self.read_double(), self.read_double(), self.read_double(), self.read_int(),
            self.read_int(), self.read_boolean()
        )

    def write_car(self, car):
        if car is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_long(car.id)
            self.write_double(car.mass)
            self.write_double(car.x)
            self.write_double(car.y)
            self.write_double(car.speed_x)
            self.write_double(car.speed_y)
            self.write_double(car.angle)
            self.write_double(car.angular_speed)
            self.write_double(car.width)
            self.write_double(car.height)
            self.write_long(car.player_id)
            self.write_int(car.teammate_index)
            self.write_boolean(car.teammate)
            self.write_enum(car.type)
            self.write_int(car.projectile_count)
            self.write_int(car.nitro_charge_count)
            self.write_int(car.oil_canister_count)
            self.write_int(car.remaining_projectile_cooldown_ticks)
            self.write_int(car.remaining_nitro_cooldown_ticks)
            self.write_int(car.remaining_oil_cooldown_ticks)
            self.write_int(car.remaining_nitro_ticks)
            self.write_int(car.remaining_oiled_ticks)
            self.write_double(car.durability)
            self.write_double(car.engine_power)
            self.write_double(car.wheel_turn)
            self.write_int(car.next_waypoint_x)
            self.write_int(car.next_waypoint_y)
            self.write_boolean(car.finished_track)

    def read_cars(self):
        car_count = self.read_int()
        if car_count < 0:
            return None

        cars = []

        for _ in range(car_count):
            cars.append(self.read_car())

        return cars

    def write_cars(self, cars):
        if cars is None:
            self.write_int(-1)
        else:
            self.write_int(cars.__len__())

            for car in cars:
                self.write_car(car)

    def read_game(self):
        if not self.read_boolean():
            return None

        return Game(
            self.read_long(), self.read_int(), self.read_int(), self.read_int(), self.read_double(), self.read_double(),
            self.read_int(), self.read_int(), self.read_int(), self.read_double(), self.read_ints(), self.read_int(),
            self.read_double(), self.read_double(), self.read_int(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_int(), self.read_int(),
            self.read_int(), self.read_double(), self.read_int(), self.read_int(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_int(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_int(), self.read_int()
        )

    def write_game(self, game):
        if game is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_long(game.random_seed)
            self.write_int(game.tick_count)
            self.write_int(game.world_width)
            self.write_int(game.world_height)
            self.write_double(game.track_tile_size)
            self.write_double(game.track_tile_margin)
            self.write_int(game.lap_count)
            self.write_int(game.lap_tick_count)
            self.write_int(game.initial_freeze_duration_ticks)
            self.write_double(game.burning_time_duration_factor)
            self.write_ints(game.finish_track_scores)
            self.write_int(game.finish_lap_score)
            self.write_double(game.lap_waypoints_summary_score_factor)
            self.write_double(game.car_damage_score_factor)
            self.write_int(game.car_elimination_score)
            self.write_double(game.car_width)
            self.write_double(game.car_height)
            self.write_double(game.car_engine_power_change_per_tick)
            self.write_double(game.car_wheel_turn_change_per_tick)
            self.write_double(game.car_angular_speed_factor)
            self.write_double(game.car_movement_air_friction_factor)
            self.write_double(game.car_rotation_air_friction_factor)
            self.write_double(game.car_lengthwise_movement_friction_factor)
            self.write_double(game.car_crosswise_movement_friction_factor)
            self.write_double(game.car_rotation_friction_factor)
            self.write_int(game.throw_projectile_cooldown_ticks)
            self.write_int(game.use_nitro_cooldown_ticks)
            self.write_int(game.spill_oil_cooldown_ticks)
            self.write_double(game.nitro_engine_power_factor)
            self.write_int(game.nitro_duration_ticks)
            self.write_int(game.car_reactivation_time_ticks)
            self.write_double(game.buggy_mass)
            self.write_double(game.buggy_engine_forward_power)
            self.write_double(game.buggy_engine_rear_power)
            self.write_double(game.jeep_mass)
            self.write_double(game.jeep_engine_forward_power)
            self.write_double(game.jeep_engine_rear_power)
            self.write_double(game.bonus_size)
            self.write_double(game.bonus_mass)
            self.write_int(game.pure_score_amount)
            self.write_double(game.washer_radius)
            self.write_double(game.washer_mass)
            self.write_double(game.washer_initial_speed)
            self.write_double(game.washer_damage)
            self.write_double(game.side_washer_angle)
            self.write_double(game.tire_radius)
            self.write_double(game.tire_mass)
            self.write_double(game.tire_initial_speed)
            self.write_double(game.tire_damage_factor)
            self.write_double(game.tire_disappear_speed_factor)
            self.write_double(game.oil_slick_initial_range)
            self.write_double(game.oil_slick_radius)
            self.write_int(game.oil_slick_lifetime)
            self.write_int(game.max_oiled_state_duration_ticks)

    def read_games(self):
        game_count = self.read_int()
        if game_count < 0:
            return None

        games = []

        for _ in range(game_count):
            games.append(self.read_game())

        return games

    def write_games(self, games):
        if games is None:
            self.write_int(-1)
        else:
            self.write_int(games.__len__())

            for game in games:
                self.write_game(game)

    def read_move(self):
        if not self.read_boolean():
            return None

        move = Move()

        move.engine_power = self.read_double()
        move.brake = self.read_boolean()
        move.wheel_turn = self.read_double()
        move.throw_projectile = self.read_boolean()
        move.use_nitro = self.read_boolean()
        move.spill_oil = self.read_boolean()

        return move

    def write_move(self, move):
        if move is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_double(move.engine_power)
            self.write_boolean(move.brake)
            self.write_double(move.wheel_turn)
            self.write_boolean(move.throw_projectile)
            self.write_boolean(move.use_nitro)
            self.write_boolean(move.spill_oil)

    def read_moves(self):
        move_count = self.read_int()
        if move_count < 0:
            return None

        moves = []

        for _ in range(move_count):
            moves.append(self.read_move())

        return moves

    def write_moves(self, moves):
        if moves is None:
            self.write_int(-1)
        else:
            self.write_int(moves.__len__())

            for move in moves:
                self.write_move(move)

    def read_oil_slick(self):
        if not self.read_boolean():
            return None

        return OilSlick(
            self.read_long(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_int()
        )

    def write_oil_slick(self, oil_slick):
        if oil_slick is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_long(oil_slick.id)
            self.write_double(oil_slick.mass)
            self.write_double(oil_slick.x)
            self.write_double(oil_slick.y)
            self.write_double(oil_slick.speed_x)
            self.write_double(oil_slick.speed_y)
            self.write_double(oil_slick.angle)
            self.write_double(oil_slick.angular_speed)
            self.write_double(oil_slick.radius)
            self.write_int(oil_slick.remaining_lifetime)

    def read_oil_slicks(self):
        oil_slick_count = self.read_int()
        if oil_slick_count < 0:
            return None

        oil_slicks = []

        for _ in range(oil_slick_count):
            oil_slicks.append(self.read_oil_slick())

        return oil_slicks

    def write_oil_slicks(self, oil_slicks):
        if oil_slicks is None:
            self.write_int(-1)
        else:
            self.write_int(oil_slicks.__len__())

            for oil_slick in oil_slicks:
                self.write_oil_slick(oil_slick)

    def read_player(self):
        if not self.read_boolean():
            return None

        return Player(self.read_long(), self.read_boolean(), self.read_string(), self.read_boolean(), self.read_int())

    def write_player(self, player):
        if player is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_long(player.id)
            self.write_boolean(player.me)
            self.write_string(player.name)
            self.write_boolean(player.strategy_crashed)
            self.write_int(player.score)

    def read_players(self):
        player_count = self.read_int()
        if player_count < 0:
            return None

        players = []

        for _ in range(player_count):
            players.append(self.read_player())

        return players

    def write_players(self, players):
        if players is None:
            self.write_int(-1)
        else:
            self.write_int(players.__len__())

            for player in players:
                self.write_player(player)

    def read_player_context(self):
        if not self.read_boolean():
            return None

        return PlayerContext(self.read_cars(), self.read_world())

    def write_player_context(self, player_context):
        if player_context is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_cars(player_context.cars)
            self.write_world(player_context.world)

    def read_player_contexts(self):
        player_context_count = self.read_int()
        if player_context_count < 0:
            return None

        player_contexts = []

        for _ in range(player_context_count):
            player_contexts.append(self.read_player_context())

        return player_contexts

    def write_player_contexts(self, player_contexts):
        if player_contexts is None:
            self.write_int(-1)
        else:
            self.write_int(player_contexts.__len__())

            for player_context in player_contexts:
                self.write_player_context(player_context)

    def read_projectile(self):
        if not self.read_boolean():
            return None

        return Projectile(
            self.read_long(), self.read_double(), self.read_double(), self.read_double(), self.read_double(),
            self.read_double(), self.read_double(), self.read_double(), self.read_double(), self.read_long(),
            self.read_long(), self.read_enum(ProjectileType)
        )

    def write_projectile(self, projectile):
        if projectile is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_long(projectile.id)
            self.write_double(projectile.mass)
            self.write_double(projectile.x)
            self.write_double(projectile.y)
            self.write_double(projectile.speed_x)
            self.write_double(projectile.speed_y)
            self.write_double(projectile.angle)
            self.write_double(projectile.angular_speed)
            self.write_double(projectile.radius)
            self.write_long(projectile.car_id)
            self.write_long(projectile.player_id)
            self.write_enum(projectile.type)

    def read_projectiles(self):
        projectile_count = self.read_int()
        if projectile_count < 0:
            return None

        projectiles = []

        for _ in range(projectile_count):
            projectiles.append(self.read_projectile())

        return projectiles

    def write_projectiles(self, projectiles):
        if projectiles is None:
            self.write_int(-1)
        else:
            self.write_int(projectiles.__len__())

            for projectile in projectiles:
                self.write_projectile(projectile)

    def read_world(self):
        if not self.read_boolean():
            return None

        return World(
            self.read_int(), self.read_int(), self.read_int(), self.read_int(), self.read_int(), self.read_players(),
            self.read_cars(), self.read_projectiles(), self.read_bonuses(), self.read_oil_slicks(),
            self.read_map_name(), self.read_tiles_x_y(), self.read_waypoints(), self.read_starting_direction()
        )

    def write_world(self, world):
        if world is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)

            self.write_int(world.tick)
            self.write_int(world.tick_count)
            self.write_int(world.last_tick_index)
            self.write_int(world.width)
            self.write_int(world.height)
            self.write_players(world.players)
            self.write_cars(world.cars)
            self.write_projectiles(world.projectiles)
            self.write_bonuses(world.bonuses)
            self.write_oil_slicks(world.oil_slicks)
            self.write_string(world.map_name)
            self.write_enums_2d(world.tiles_x_y)
            self.write_ints_2d(world.waypoints)
            self.write_enum(world.starting_direction)

    def read_worlds(self):
        world_count = self.read_int()
        if world_count < 0:
            return None

        worlds = []

        for _ in range(world_count):
            worlds.append(self.read_world())

        return worlds

    def write_worlds(self, worlds):
        if worlds is None:
            self.write_int(-1)
        else:
            self.write_int(worlds.__len__())

            for world in worlds:
                self.write_world(world)

    def read_map_name(self):
        if self.map_name is None:
            self.map_name = self.read_string()

        return self.map_name

    def read_tiles_x_y(self):
        if self.tiles_x_y is None:
            self.tiles_x_y = self.read_enums_2d(TileType)

        return self.tiles_x_y

    def read_waypoints(self):
        if self.waypoints is None:
            self.waypoints = self.read_ints_2d()

        return self.waypoints

    def read_starting_direction(self):
        if self.starting_direction is None:
            self.starting_direction = self.read_enum(Direction)

        return self.starting_direction

    @staticmethod
    def ensure_message_type(actual_type, expected_type):
        if actual_type != expected_type:
            raise ValueError("Received wrong message [actual=%s, expected=%s]." % (actual_type, expected_type))

    def read_enum(self, enum_class):
        byte_array = self.read_bytes(RemoteProcessClient.SIGNED_BYTE_SIZE_BYTES)
        value = struct.unpack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "b", byte_array)[0]

        for enum_key, enum_value in enum_class.__dict__.items():
            if not str(enum_key).startswith("__") and value == enum_value:
                return enum_value

        return None

    def read_enums(self, enum_class):
        count = self.read_int()
        if count < 0:
            return None

        enums = []

        for _ in range(count):
            enums.append(self.read_enum(enum_class))

        return enums

    def read_enums_2d(self, enum_class):
        count = self.read_int()
        if count < 0:
            return None

        enums_2d = []

        for _ in range(count):
            enums_2d.append(self.read_enums(enum_class))

        return enums_2d

    def write_enum(self, value):
        self.write_bytes(struct.pack(
            RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "b", -1 if value is None else value
        ))

    def write_enums(self, enums):
        if enums is None:
            self.write_int(-1)
        else:
            self.write_int(enums.__len__())

            for value in enums:
                self.write_enum(value)

    def write_enums_2d(self, enums_2d):
        if enums_2d is None:
            self.write_int(-1)
        else:
            self.write_int(enums_2d.__len__())

            for enums in enums_2d:
                self.write_enums(enums)

    def read_string(self):
        length = self.read_int()
        if length == -1:
            return None

        byte_array = self.read_bytes(length)
        return byte_array.decode()

    def write_string(self, value):
        if value is None:
            self.write_int(-1)
            return

        byte_array = value.encode()

        self.write_int(len(byte_array))
        self.write_bytes(byte_array)

    def read_boolean(self):
        byte_array = self.read_bytes(RemoteProcessClient.SIGNED_BYTE_SIZE_BYTES)
        return struct.unpack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "b", byte_array)[0] != 0

    def read_boolean_array(self, count):
        byte_array = self.read_bytes(count * RemoteProcessClient.SIGNED_BYTE_SIZE_BYTES)
        unpacked_bytes = struct.unpack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + str(count) + "b", byte_array)

        return [unpacked_bytes[i] != 0 for i in range(count)]

    def write_boolean(self, value):
        self.write_bytes(struct.pack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "b", 1 if value else 0))

    def read_int(self):
        byte_array = self.read_bytes(RemoteProcessClient.INTEGER_SIZE_BYTES)
        return struct.unpack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "i", byte_array)[0]

    def read_ints(self):
        count = self.read_int()
        if count < 0:
            return None

        ints = []

        for _ in range(count):
            ints.append(self.read_int())

        return ints

    def read_ints_2d(self):
        count = self.read_int()
        if count < 0:
            return None

        ints_2d = []

        for _ in range(count):
            ints_2d.append(self.read_ints())

        return ints_2d

    def write_int(self, value):
        self.write_bytes(struct.pack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "i", value))

    def write_ints(self, ints):
        if ints is None:
            self.write_int(-1)
        else:
            self.write_int(ints.__len__())

            for value in ints:
                self.write_int(value)

    def write_ints_2d(self, ints_2d):
        if ints_2d is None:
            self.write_int(-1)
        else:
            self.write_int(ints_2d.__len__())

            for ints in ints_2d:
                self.write_ints(ints)

    def read_long(self):
        byte_array = self.read_bytes(RemoteProcessClient.LONG_SIZE_BYTES)
        return struct.unpack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "q", byte_array)[0]

    def write_long(self, value):
        self.write_bytes(struct.pack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "q", value))

    def read_double(self):
        byte_array = self.read_bytes(RemoteProcessClient.DOUBLE_SIZE_BYTES)
        return struct.unpack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "d", byte_array)[0]

    def write_double(self, value):
        self.write_bytes(struct.pack(RemoteProcessClient.BYTE_ORDER_FORMAT_STRING + "d", value))

    def read_bytes(self, byte_count):
        byte_array = bytes()

        while len(byte_array) < byte_count:
            chunk = self.socket.recv(byte_count - len(byte_array))

            if not len(chunk):
                raise IOError("Can't read %s bytes from input stream." % str(byte_count))

            byte_array += chunk

        return byte_array

    def write_bytes(self, byte_array):
        self.socket.sendall(byte_array)

    class MessageType:
        UNKNOWN = 0
        GAME_OVER = 1
        AUTHENTICATION_TOKEN = 2
        TEAM_SIZE = 3
        PROTOCOL_VERSION = 4
        GAME_CONTEXT = 5
        PLAYER_CONTEXT = 6
        MOVE = 7
