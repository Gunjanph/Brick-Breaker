import os
from props import Props

class Paddle(Props):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.shape = ["I", "I", "I", "I", "I", "I", "I"]

    def starting_position(self, grid):
        for i in range(len(self.shape)):
            grid[28][47+i] = self.shape[i]
    
    def get_y(self):
        return self.y
    
    def get_len(self):
        return len(self.shape)
    
    def expand(self):
        for i in range(2):
            self.shape.append("I")

    def shrink(self):
        length = len(self.shape)
        for i in range(2):
            self.shape.pop(length-i-1)

    def right_collision(self, xcoo, velx):
        if self.y + 2 < 109-len(self.shape):
            if xcoo == 27 and velx == 0:
                return 1
            else:
                return 2
        else:
            return 0
    
    def left_collision(self, xcoo, velx):
        if self.y - 2 >= 0:
            if xcoo == 27 and velx == 0:
                return 1
            else:
                return 2
        else:
            return 0
    
    def disappear_paddle(self, obj_board):
        for i in range(len(self.shape)):
            obj_board.matrix[28][self.y+i] = " "
    
    def reappear_paddle(self, obj_board):
        for i in range(len(self.shape)):
            obj_board.matrix[28][self.y+i] = self.shape[i]