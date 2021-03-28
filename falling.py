import os
from random import randrange, randint
from colorama import init, Fore, Back
from config import Config
init()
from bricks import Bricks

class Falling_Brick(Bricks):
    def __init__(self):
        super().__init__()

    def fall_appear_brick(self, obj_board):
        for i in range(obj_board.rows-1, -1, -1):
            for j in range(obj_board.columns):
                if obj_board.matrix[i][j] == "X":
                    # print(i,j)
                    if i+1 == 28:
                        print("GAME OVER :'(")
                        quit()
                    obj_board.matrix[i+1][j] = "X"
                    obj_board.matrix[i+1][j+1] = obj_board.matrix[i][j+1]
                    obj_board.matrix[i][j+1] = " "
                    obj_board.matrix[i][j] = " "