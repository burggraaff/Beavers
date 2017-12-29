# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:01:41 2017

@author: Olivier
"""

import numpy as np
import random


class Card(object):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class SpecialCard(Card):
    def __init__(self, name):
        Card.__init__(self, name)

        if name == "swap":
            self.func = SpecialCard.swap
        elif name == "double":
            self.func = SpecialCard.double
        elif name == "look":
            self.func = SpecialCard.look
        else:
            raise ValueError("Invalid `name` parameter for SpecialCard")

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
            self.take_pile.extend(SpecialCard(name) for j in range(5))
        random.shuffle(self.take_pile)

    def give(self):
        return self.take_pile.pop()

    def __repr__(self):
        #return "Take: {0} ; Discard: {1}".format(len(self.take_pile), len(self.discard_pile))
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
        self.stack = Stack()
        self.game.active_round = self

        for player in self.players:
            start_hand = [self.stack.give() for i in range(4)]
            player.deal_hand(start_hand)

    def end(self):
        scores = [player.score() for player in self.players]

        self.active = False
        return scores


class Game(object):
    def __init__(self, nrplayers):
        self.players = [Player("Player{0}".format(i+1)) for i in range(nrplayers)]
        self.rounds = [Round(self, self.players) for i in range(nrplayers)]
        self.scores = np.zeros((len(self.rounds), len(self.players)), dtype = int)
        self.final_scores = np.zeros(len(self.players), dtype = int)
        self.active_round = None

        self.rounds[0].activate()

    def __repr__(self):
        return "Game \nPlayers: {p}\nScores:\n{s}\nFinal scores:\n{f}".format(p = self.players, s = self.scores, f = self.final_scores)