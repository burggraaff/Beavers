# -*- coding: utf-8 -*-

from .cards import Stack
from .players import Human, AI

import numpy as np
from itertools import cycle


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
            if j > 1:
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
        self.players = [Human("Player1")] + [AI(f"Player{i+2}") for i in range(nrplayers)]
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
