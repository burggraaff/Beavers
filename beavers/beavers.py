# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:01:41 2017

@author: Olivier
"""

import numpy as np
from random import shuffle


class Card(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class SpecialCard(Card):
    def __init__(self, name):
        assert name in ("look", "double", "swap")
        Card.__init__(self, name)

    @staticmethod
    def swap():
        pass

    @staticmethod
    def double():
        pass

    @staticmethod
    def look():
        pass


class Stack(object):
    def __init__(self):
        self.take_pile = []
        self.discard_pile = []
        for i in range(9):
            self.take_pile.extend(Card(i) for j in range(4))
        self.take_pile.extend(Card(9) for j in range(9))
        for name in ("swap", "double", "look"):
            self.take_pile.extend(SpecialCard(name) for j in range(6))
        shuffle(self.take_pile)

    def give(self):
        return self.take_pile.pop()

    def draw(self):
        if len(self.take_pile) == 0:  # if no cards are left, shuffle
            shuffle(self.discard_pile)
            self.take_pile = self.discard_pile
            self.discard_pile = []
        self.discard_pile.append(self.take_pile.pop())

    def take_top(self):
        print(self.take_pile[-1])

    def disc_top(self):
        print(self.discard_pile[-1])

    def __repr__(self):
        return f"Take: {len(self.take_pile)} ; Discard: {len(self.discard_pile)}"


class Hand(list):
    def __init__(self, cards):
        list.__init__(self)
        assert len(cards) == 4
        self.extend(cards)


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = None

    def deal_hand(self, cards):
        self.hand = Hand(cards)

    def __repr__(self):
        return self.name

    def score(self):
        return self.hand.score()


class Round(object):
    def __init__(self, game, players):
        self.game = game
        self.players = players

        self.active = False

    def __repr__(self):
        if self.active:
            return "Active round"
        else:
            return "Inactive round"

    def activate(self):
        self.active = True
        self.to_end = False
        self.stack = Stack()
        self.game.active_round = self

        for player in self.players:
            start_hand = [self.stack.give() for i in range(4)]
            player.deal_hand(start_hand)

        self.stack.draw()

    def end(self):
        scores = [player.score() for player in self.players]

        self.active = False
        return scores


class Game(object):
    def __init__(self, nrplayers):
        assert 3 <= nrplayers <= 6
        self.players = [Player(f"Player{i+1}") for i in range(nrplayers)]
        self.rounds = [Round(self, self.players) for i in range(nrplayers)]
        self.scores = np.zeros((len(self.rounds), len(self.players)), dtype=int)
        self.final_scores = np.zeros(len(self.players), dtype=int)
        self.active_round = None

        self.rounds[0].activate()

    def __repr__(self):
        return f"Game \nPlayers: {self.players}\nScores:\n{self.scores}\nFinal scores:\n{self.final_scores}"
