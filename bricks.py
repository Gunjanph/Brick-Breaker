import os
from random import randrange, randint
from colorama import init, Fore, Back
from config import Config
init()

brick_config = Config()
# Parent
class Bricks:
    def __init__(self):
        self.bricks = "X"
        self.strength = 0

    def strength(self):
        return self.strength

# Child
class Brick(Bricks):
    def __init__(self):
        super().__init__()
        self.strength = 1

    def strength(self):
        return self.strength

    def appear_brick(self, grid, level, flag):
        if level == 1:
            # print(brick_config.level)
            for i in range(6,11,4):
                for j in range(30,80,2):
                    grid[i][j] = self.bricks
                for j in range(31,81,2):
                    grid[i][j] = 1
            
            for i in range(7,10,2):
                for j in range(34,76,2):
                    # if j!=52 and j!=54 and j!=56:
                    grid[i][j] = self.bricks
                for j in range(35,77,2):
                    # if j!=53 and j!=55 and j!=57:
                    grid[i][j] = 2

            for i in range(38,72,2):
                grid[8][i] = self.bricks
            for i in range(39,73,2):
                    grid[8][i] = 3
        if level == 2:
            # print(brick_config.level)
            for i in range(6,11,4):
                for j in range(34,76,2):
                    grid[i][j] = self.bricks
                for j in range(35,77,2):
                    grid[i][j] = 3
            for i in range(7, 10,1):
                for j in range(34,76, 40):
                    grid[i][j] = self.bricks
                for j in range(35,77, 40):
                    grid[i][j] = 3
            
            for i in range(7,10,2):
                for j in range(36,74,2):
                    # if j!=52 and j!=54 and j!=56:
                    grid[i][j] = self.bricks
                for j in range(37,75,2):
                    # if j!=53 and j!=55 and j!=57:
                    grid[i][j] = 2
            for i in range(8, 9,1):
                for j in range(36,74, 36):
                    grid[i][j] = self.bricks
                for j in range(37,75, 36):
                    grid[i][j] = 2

            for i in range(38,72,2):
                grid[8][i] = self.bricks
            for i in range(39,73,2):
                grid[8][i] = 1
        
        if level == 3 and flag == 1:
            for j in range(0, 110):
                if j%2==0:
                    grid[15][j] = self.bricks
                else:
                    grid[15][j] = 1 

    def disappear_brick(self, obj_board, x, y, obj_config):
        numb = 0
        # print(obj_board.matrix[x][y+1])
        if obj_board.matrix[x][y+1] == 1:
            obj_board.matrix[x][y] = " "
            # print("in disappear: "+ obj_board.matrix[x][y])
            prob = randint(0,1)
            # prob = 1
            if prob == 1:
                numb = randrange(1,6)
                # numb = 6
            obj_config.score += 1
        if obj_board.matrix[x][y+1] == 2:
            obj_board.matrix[x][y+1] = 1
            obj_config.score += 1
        if obj_board.matrix[x][y+1] == 3:
            obj_board.matrix[x][y+1] = 2
            obj_config.score += 1
        return numb

    def level_disappear_brick(self, obj_board):
        for i in range(obj_board.rows):
            for j in range(obj_board.columns):
                if obj_board.matrix[i][j] == "X":
                    obj_board.matrix[i][j] = " "


# class Brick2(Bricks):
#     def __init__(self):
#         super().__init__()
#         self.strength = 2

#     def strength(self):
#         return self.strength

#     def appear_brick2(self, grid):
#         for i in range(7,10,2):
#             for j in range(34,76,2):
#                 grid[i][j] = self.bricks
#             for j in range(35,77,2):
#                 grid[i][j] = self.strength
        
#         # for i in range(42, 68, 26):
#         #     grid[8][i] = self.bricks

# class Brick3(Bricks):
#     def __init__(self):
#         super().__init__()
#         self.strength = 3

#     def strength(self):
#         return self.strength

#     def appear_brick3(self, grid):
#         for i in range(38,72,2):
#             grid[8][i] = self.bricks
#         for i in range(39,73,2):
#                 grid[8][i] = self.strength

class UnbreakableBrick(Bricks):
    def __init__(self):
        super().__init__()
        self.strength = 5

    def strength(self):
        return self.strength

    def appear_unb(self, grid, level):
        if level == 1:
            for i in range(20,90,2):
                grid[5][i] = self.bricks
            for i in range(21,91,2):
                    grid[5][i] = self.strength
        if level == 2:
            for i in range(32,78,2):
                grid[5][i] = self.bricks
            for i in range(33,79,2):
                    grid[5][i] = self.strength

            for i in range(6,11):
                for j in range(32, 78, 44):
                    grid[i][j] = self.bricks
                for j in range(33, 79, 44):
                    grid[i][j] = self.strength