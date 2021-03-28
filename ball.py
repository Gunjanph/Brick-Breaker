import os
from props import Props

class Ball(Props):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.shape = "o"
        self.number = 1
        self.vely = 0
        self.velx = 0
        self.active = 0
        self.thruactive = 0

    def starting_position(self, grid):
        grid[27][self.y] = self.shape

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_velx(self):
        return self.velx
    
    def get_vely(self):
        return self.vely
    
    def disappear_ball(self, obj_board):
        obj_board.matrix[self.x][self.y] = " "
    
    def reappear_ball(self, obj_board):
        obj_board.matrix[self.x][self.y] = self.shape