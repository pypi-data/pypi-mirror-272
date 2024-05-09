#!/usr/bin/python3

class Player:

    def __init__(self, name, nation, gs):

        self.name = name
        self.nation = nation
        self.gs = gs

    def __repr__(self):

        return f"{self.name} ({self.nation}) Grand Slams: {self.gs}"


big_three = [
    Player("Rafa Nadal", "Spain", 22),
    Player("Roger Federer", "Switzerland", 20),
    Player("Novak Djokovic", "Serbia", 24),
]


def list_players():

    for player in big_three:
        print(player)


def search_player(name):

    for player in big_three:
        if player.name == name:
            return player

    return None

