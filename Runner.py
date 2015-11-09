import sys

from MyStrategy import MyStrategy
from RemoteProcessClient import RemoteProcessClient
from model.Move import Move


class Runner:
    def __init__(self):
        if sys.argv.__len__() == 4:
            self.remote_process_client = RemoteProcessClient(sys.argv[1], int(sys.argv[2]))
            self.token = sys.argv[3]
        else:
            self.remote_process_client = RemoteProcessClient("127.0.0.1", 31001)
            self.token = "0000000000000000"

    def run(self):
        try:
            self.remote_process_client.write_token_message(self.token)
            team_size = self.remote_process_client.read_team_size_message()
            self.remote_process_client.write_protocol_version_message()
            game = self.remote_process_client.read_game_context_message()

            strategies = []

            for _ in range(team_size):
                strategies.append(MyStrategy())

            while True:
                player_context = self.remote_process_client.read_player_context_message()
                if player_context is None:
                    break

                player_cars = player_context.cars
                if player_cars is None or player_cars.__len__() != team_size:
                    break

                moves = []

                for car_index in range(team_size):
                    player_car = player_cars[car_index]

                    move = Move()
                    moves.append(move)
                    strategies[player_car.teammate_index].move(player_car, player_context.world, game, move)

                self.remote_process_client.write_moves_message(moves)
        finally:
            self.remote_process_client.close()


Runner().run()
