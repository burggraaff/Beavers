# -*- coding: utf-8 -*-

from ..cards import Hand


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = None

    def deal_hand(self, cards, stack):
        self.hand = Hand(cards, stack)

    def __repr__(self):
        return f"{self.name} ({self.__class__.__name__})"

    def score(self):
        return self.hand.score()

    def play(self, r):
        raise NotImplementedError(f"{self.__class__} has not implemented `play`")
