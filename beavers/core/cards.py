# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 02:10:49 2017

@author: Olivier
"""

from random import shuffle


class Card(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other.value

    def __radd__(self, other):
        return self.value + other


class SpecialCard(Card):
    def __init__(self, name):
        assert name in ("look", "double", "swap")
        super().__init__(name)

    @staticmethod
    def swap():
        pass

    @staticmethod
    def double():
        pass

    @staticmethod
    def look():
        pass


class Hand(list):
    def __init__(self, cards, stack):
        super().__init__()
        self.stack = stack
        assert len(cards) == 4
        self.extend(cards)

    def score(self):
        for j, card in enumerate(self):
            this_card = card
            while isinstance(this_card, SpecialCard):
                # keep drawing cards until all special cards have been replaced
                this_card = self.stack.give()
            self[j] = this_card
        return sum(self)


class Stack(object):
    def __init__(self):
        self.take_pile = []
        self.discard_pile = []
        for i in range(9):
            self.take_pile.extend(Card(i) for j in range(4))
        self.take_pile.extend(Card(9) for j in range(9))
        self.take_pile.extend(SpecialCard("swap") for j in range(9))
        self.take_pile.extend(SpecialCard("look") for j in range(7))
        self.take_pile.extend(SpecialCard("double") for j in range(5))
        shuffle(self.take_pile)

    def give(self):
        self.check_shuffle()
        return self.take_pile.pop()

    def give_from_discard(self):
        assert len(self.discard_pile)
        return self.discard_pile.pop()

    def draw(self):
        self.check_shuffle()
        self.discard_pile.append(self.take_pile.pop())

    def discard(self, card):
        self.discard_pile.append(card)

    def check_shuffle(self):
        if len(self.take_pile) == 0:  # if no cards are left, shuffle
            shuffle(self.discard_pile)
            self.take_pile = self.discard_pile
            self.discard_pile = []

    def take_top(self):
        return self.take_pile[-1]

    def disc_top(self):
        return self.discard_pile[-1]

    def __repr__(self):
        nr_take = len(self.take_pile)
        nr_disc = len(self.discard_pile)
        return f"T {nr_take}, D {nr_disc} ({nr_take + nr_disc})"
