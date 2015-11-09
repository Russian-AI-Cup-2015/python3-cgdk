from model.Car import Car
from model.Game import Game
from model.Move import Move
from model.World import World


class MyStrategy:
    def move(self, me: Car, world: World, game: Game, move: Move):
        move.engine_power = 1.0
        move.throw_projectile = True
        move.spill_oil = True

        if world.tick > game.initial_freeze_duration_ticks:
            move.use_nitro = True
