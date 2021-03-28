import os
from colorama import init, Fore, Back
init()
from props import Props

class Bomb(Props):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.shape = "|"
        self.vely = 0
        self.velx = 1
    
    def starting_position(self, grid, x, y):
        grid[x][y] = self.shape
    
    def disappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = " "
    
    def reappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = self.shape
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_velx(self):
        return self.velx
    
    def get_vely(self):
        return self.vely