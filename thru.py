import os
from colorama import init, Fore, Back
init()
from powerup import Powerup

class Thru(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = "t"
        self.number = 5
        self.time = 10
    
    def starting_position(self, grid, x, y):
        grid[self.x][self.y] = self.shape
    
    def disappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = " "
    
    def reappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = self.shape