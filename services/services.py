from random import sample, choice
from os import listdir
from datetime import datetime


class Player:
    def __init__(self, username: int) -> None:
        self.username = username
        self.specifications = []
        self.open_specifications = []
        self.in_game = False


class Room:
    def __init__(self, player: Player) -> None:
        self.players = [player]
        self.round = 0
        self.active_player = None

    def next_active_player(self):
        for i in range(len(self)):
            if self.players[i].username == self.active_player.username:
                self.active_player = self.players[(i + 1) % len(self)]
                break

    def __len__(self):
        return len(self.players)


def get_roles(lenn):
    lis = [
        map(
            lambda x: "JPG\\Профессия" + "\\" + x,
            sample(listdir("JPG\\Профессия"), lenn),
        ),
        map(
            lambda x: "JPG\\Биология" + "\\" + x, sample(listdir("JPG\\Биология"), lenn)
        ),
        map(
            lambda x: "JPG\\Здоровье" + "\\" + x, sample(listdir("JPG\\Здоровье"), lenn)
        ),
        map(lambda x: "JPG\\Хобби" + "\\" + x, sample(listdir("JPG\\Хобби"), lenn)),
        map(lambda x: "JPG\\Багаж" + "\\" + x, sample(listdir("JPG\\Багаж"), lenn)),
        map(lambda x: "JPG\\Факты" + "\\" + x, sample(listdir("JPG\\Факты"), lenn)),
        # map(
        #     lambda x: "JPG\\Особые условия" + "\\" + x,
        #     sample(listdir("JPG\\Особые условия"), lenn),
        # ),
    ]
    return list(zip(*lis))


def get_kat():
    return "JPG\\Катастрофа" + "\\" + choice(listdir("JPG\\Катастрофа"))


def generate_id():
    return str(int(datetime.now().timestamp()) % 100000000)


rooms: dict[str, Room] = {}
rounds_dict = {
    4: {1: 0, 2: 0, 3: 1, 4: 1},
    5: {1: 0, 2: 1, 3: 1, 4: 1},
    6: {1: 0, 2: 1, 3: 1, 4: 1},
    7: {1: 1, 2: 1, 3: 1, 4: 1},
    8: {1: 1, 2: 1, 3: 1, 4: 1},
    9: {1: 1, 2: 1, 3: 1, 4: 2},
    10: {1: 1, 2: 1, 3: 1, 4: 2},
    11: {1: 1, 2: 1, 3: 2, 4: 2},
    12: {1: 1, 2: 1, 3: 2, 4: 2},
    13: {1: 1, 2: 2, 3: 2, 4: 2},
    14: {1: 1, 2: 2, 3: 2, 4: 2},
    15: {1: 2, 2: 2, 3: 2, 4: 2},
    16: {1: 2, 2: 2, 3: 2, 4: 2},
}
