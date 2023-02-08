import os
from colorama import init, Fore, Back
init()
import numpy as np
from props import Props

class Boss(Props):

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        a = np.zeros((9, 40), dtype='<U20')
        a[:] = ' '
        self.j = 0
        self.i = 0
        self.health = 100
        with open("ufo.txt") as obj:
            for line in obj:
                self.i = 0
                for char in line:
                    if char == '\n':
                        break
                    else:
                        a[self.j][self.i] = char
                    self.i += 1
                self.j += 1
        self.shape = a

    def starting_position(self, grid):
        for k in range(self.j):
            for l in range(39):
                grid[self.x+k][self.y+l] = self.shape[k][l]

    def appear_boss(self,obj_board):
        for k in range(self.j):
            for l in range(39):
                obj_board.matrix[self.x+k][self.y+l] = self.shape[k][l]

    def disappear_boss(self,obj_board):
        for k in range(self.j):
            for l in range(39):
                obj_board.matrix[self.x+k][self.y+l] = " "


