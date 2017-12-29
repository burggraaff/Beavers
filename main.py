# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:58:45 2017

@author: Olivier
"""

import beavers as b
import sys

nrplayers = int(sys.argv[1])

game = b.Game(nrplayers)

game.play()