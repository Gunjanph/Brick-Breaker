import os
from random import randrange, randint
from colorama import init, Fore, Back
from config import Config
init()
from bricks import Bricks

class Rainbow_Brick(Bricks):
    def __init__(self):
        super().__init__()

    def rainbow_appear_brick(self, obj_board):
        obj_board.matrix[6][20] = self.bricks
        obj_board.matrix[6][21] = 1
    
    def color(self, obj_board):
        if obj_board.matrix[6][21]==3:
            obj_board.matrix[6][21]=1
        else:
            obj_board.matrix[6][21]+=1
