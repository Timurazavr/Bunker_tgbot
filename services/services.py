from random import sample
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
        self.active_player = []


def get_roles(lenn):
    lis = [
        sample(listdir("JPG\\Профессия"), lenn),
        sample(listdir("JPG\\Биология"), lenn),
        sample(listdir("JPG\\Здоровье"), lenn),
        sample(listdir("JPG\\Хобби"), lenn),
        sample(listdir("JPG\\Багаж"), lenn),
        sample(listdir("JPG\\Факты"), lenn),
        sample(listdir("JPG\\Особые условия"), lenn),
    ]
    return list(zip(*lis))


def generate_id():
    return int(datetime.now().timestamp()) % 100000000


rooms: dict[int, Room] = {}
sp = []
