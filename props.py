import os
from colorama import init, Fore, Back
init()

class Props:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction