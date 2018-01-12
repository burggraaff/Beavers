# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 23:42:51 2018

@author: Olivier
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label


class BeaverApp(App):
    def build(self):
        return Label(text="Beavers are cool")
