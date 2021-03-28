import os
from colorama import init, Fore, Back
init()

class Powerup:
    def __init__(self, x, y):
        self.activate = 0
        self.velx = 1
        self.vely = 0
        self.number = 0
        self.x = x
        self.y = y

    def disappear(self):
        print("Parent Disappear. So exiting........")
        quit()

    def reappear(self):
        print("Parent Deactivate. So exiting........")
        quit()