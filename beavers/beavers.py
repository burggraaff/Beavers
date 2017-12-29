# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:01:41 2017

@author: Olivier
"""

import numpy as np
from random import shuffle
from itertools import cycle


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


class Hand(list):
    def __init__(self, cards, stack):
        list.__init__(self)
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


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = None

    def deal_hand(self, cards, stack):
        self.hand = Hand(cards, stack)

    def __repr__(self):
        return self.name

    def score(self):
        return self.hand.score()

    def play(self, r):
        do = input(f"{self.name}, what do you want to do? (D: {r.stack.disc_top()})\n")
        if do == "new":
            new_card = r.stack.give()
            do_new = input(f"Replace card with {new_card}? 'no' if not\n")
            if do_new == "no":
                r.stack.discard(new_card)
            else:
                index = int(do_new)
                to_discard = self.hand[index]
                self.hand[index] = new_card
                r.stack.discard(to_discard)
        elif do == "open":
            index = int(input("Replace which card?\n"))
            to_discard = self.hand[index]
            self.hand[index] = r.stack.give_from_discard()
            r.stack.discard(to_discard)
        else:
            pass
        if r.ender is None:
            end = bool(input("End round?\n"))
            if end:
                r.ender = self
                print(f"{self.name} is ending the round!")
        print(self.hand, r.stack)


class Round(object):
    def __init__(self, game, players, number):
        self.game = game
        self.players = players
        self.number = number

        self.active = False

    def __repr__(self):
        return f"Round number {self.number} ({'' if self.active else 'in'}active)"

    def activate(self):
        self.active = True
        self.ender = None
        self.stack = Stack()
        self.game.active_round = self
        self.stack.draw()

        for player in self.players:
            start_hand = [self.stack.give() for i in range(4)]
            player.deal_hand(start_hand, self.stack)

    def play(self, first_player):
        start = self.players.index(first_player)
        self.players = self.players[start:] + self.players[:start]
        self.players_cycle = cycle(self.players)
        for j, player in enumerate(self.players_cycle):
            if player == self.ender:
                break
            player.play(self)
            if j > 10:
                break

        scores = self.end()
        return scores

    def end(self):
        scores = [player.score() for player in self.players]

        self.active = False
        print(f"End of round {self.number}!")
        return scores


class Game(object):
    def __init__(self, nrplayers):
        assert 3 <= nrplayers <= 6
        self.players = [Player(f"Player{i+1}") for i in range(nrplayers)]
        self.rounds = [Round(self, self.players, i+1) for i in range(nrplayers)]
        self.scores = []
        self.final_scores = np.zeros(len(self.players), dtype=int)
        self.rounds[0].activate()

    def play(self):
        for r, player in zip(self.rounds, self.players):
            r.activate()
            round_score = r.play(first_player=player)
            self.scores.append(round_score)
        self.scores = np.array(self.scores)
        self.final_scores = self.scores.sum(axis=0)
        print(self)

    def __repr__(self):
        line1 = f"Game on round {self.active_round.number}"
        line2 = f"Players: {self.players}"
        line3 = f"Scores: {self.scores}"
        line4 = f"Final scores: {self.final_scores}"

        lines = [line1, line2, line3, line4]
        return "\n".join(lines)  # joins lines with a line break between them
