# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.label import Label


class BeaverApp(App):
    def build(self):
        return Label(text="Beavers are cool")
