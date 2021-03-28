import os
from colorama import init, Fore, Back
init()
from powerup import Powerup

class Grab(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = "@"
        self.number = 4
        self.time = 15
    
    def starting_position(self, grid, x, y):
        grid[self.x][self.y] = self.shape
    
    def disappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = " "
    
    def reappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = self.shape