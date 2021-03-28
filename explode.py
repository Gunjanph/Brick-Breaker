import os
import time
from colorama import init, Fore, Back
init()
from bricks import Bricks

class Explode(Bricks):
    def __init__(self):
        super().__init__()
        self.strength = -10

    def exappear_brick(self, grid):
        for j in range(48,60,2):
            grid[6][j] = self.bricks
        for j in range(49,61,2):
            grid[6][j] = -10


    # isnumber use karna h!!!
    def exdisappear_brick(self, obj_board, x, y, obj_config):
        for j in range(y,109,2):
            if obj_board.matrix[x][j+1] == -10:
                # time.sleep(1)
                obj_board.matrix[x][j] = " "
                if type(obj_board.matrix[x+1][j+1]) == int:
                    obj_board.matrix[x+1][j] = " "
                    obj_config.score += obj_board.matrix[x+1][j+1]
                if type(obj_board.matrix[x-1][j+1]) == int:
                    obj_board.matrix[x-1][j] = " "
                    obj_config.score += obj_board.matrix[x-1][j+1]
            else:
                if type(obj_board.matrix[x][j+1]) == int:
                    obj_board.matrix[x][j] = " "
                    obj_config.score += obj_board.matrix[x][j+1]
                if type(obj_board.matrix[x+1][j+1]) == int:
                    obj_board.matrix[x+1][j] = " "
                    obj_config.score += obj_board.matrix[x+1][j+1]
                if type(obj_board.matrix[x-1][j+1]) == int:
                    obj_board.matrix[x-1][j] = " "
                    obj_config.score += obj_board.matrix[x-1][j+1]
                break;

        for j in range(y,0,-2):
            if obj_board.matrix[x][j+1] == -10:
                # time.sleep(1)
                obj_board.matrix[x][j] = " "
                if type(obj_board.matrix[x+1][j+1]) == int:
                    obj_board.matrix[x+1][j] = " "
                    obj_config.score += obj_board.matrix[x+1][j+1]
                if type(obj_board.matrix[x-1][j+1]) == int:
                    obj_board.matrix[x-1][j] = " "
                    obj_config.score += obj_board.matrix[x-1][j+1]
            else:
                if type(obj_board.matrix[x][j+1]) == int:
                    obj_board.matrix[x][j] = " "
                    obj_config.score += obj_board.matrix[x][j+1]
                if type(obj_board.matrix[x+1][j+1]) == int:
                    obj_board.matrix[x+1][j] = " "
                    obj_config.score += obj_board.matrix[x+1][j+1]
                if type(obj_board.matrix[x-1][j+1]) == int:
                    obj_board.matrix[x-1][j] = " "
                    obj_config.score += obj_board.matrix[x-1][j+1]
                break;