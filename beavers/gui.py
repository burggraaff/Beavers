# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 02:16:11 2017

@author: Olivier
"""

import tkinter as tk


class PlayerFrame(tk.Frame):
    def __init__(self, player):
        super().__init__(self)
        self.player = player


class Gui(tk.Tk):
    def __init__(self):
        super().__init__(self)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="NSEW")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.page = tk.Frame(master=self)
