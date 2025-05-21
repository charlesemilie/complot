import random
from typing import List
from .models import PlayerDB

class Game:
    def __init__(self, player_names: List[str]):
        self.players = [PlayerState(name) for name in player_names]
        self.deck = self._init_deck()
        self.turn_index = 0

    def _init_deck(self):
        deck = ["Duc"] * 3 + ["Assassin"] * 3 + ["Ambassadeur"] * 3 + ["Voleur"] * 3 + ["Comtesse"] * 3
        random.shuffle(deck)
        return deck

    def start(self):
        for p in self.players:
            p.hand = [self.deck.pop(), self.deck.pop()]
            p.coins = 2

    def current_player(self):
        return self.players[self.turn_index]

    def income(self):
        p = self.current_player()
        p.coins += 1
        self._next_turn()

    def foreign_aid(self):
        p = self.current_player()
        p.coins += 2
        self._next_turn()

    def coup(self, target_index: int):
        if self.current_player().coins < 7:
            raise Exception("Pas assez de pièces")
        self.current_player().coins -= 7
        self.players[target_index].lose_influence()
        self._next_turn()

    def _next_turn(self):
        self.turn_index = (self.turn_index + 1) % len(self.players)

class PlayerState:
    def __init__(self, name: str):
        self.name = name
        self.hand = []  # cartes en main
        self.coins = 0
        self.alive = True

    def lose_influence(self):
        if self.hand:
            self.hand.pop()
        if not self.hand:
            self.alive = False