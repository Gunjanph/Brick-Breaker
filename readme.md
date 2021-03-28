# Brick Breaker

An arcade game in Python3 (terminal-based), inspired from
the old classic brick breaker.

## Installation

Libraries used:
```bash
sudo apt-get update
sudo apt-get install python3
pip3 install colorama
pip3 install numpy
```
## Instructions
To play:

```bash
cd 2019111035
```
```python3
python3 main.py
```

## Rules of the Game
#### Paddle
- a - Move left
- d - Move right
#### Ball
- Space - Releases ball from paddle
#### Quit
- q - quit from the game

## Features
- Ball appears randomly on paddle in start and needs to be released.
- The collision of ball with bricks, paddle and wall is implemented.
- 3 different color bricks are implemented and unbreakable bricks are also implemented. Destroying each brick results in increase in score accordingly.
- 3 lives to win the game.
- 150 secs to win the game.
## Powerups
#### Expand
- It increases the size of paddle by 2.
- Max size could be 9
- Shape: `<==>` 
#### Shrink
- It decreases the size of paddle by 2.
- Min sizecould be 3
- Shape: `=><=` 
#### Fast
- It increases the speed of ball.
- Max speed could be 2
- Min speed could be 0
- Shape: `>>`
#### Thru
- It enables the ball to destry and go through any ball.
- Shape: `t`
#### Grab
- It allows the paddle to grab the ball on contact and relaunch the ball at will.
- Shape: `.-.`
## Bonus
*Exploding Bricks:*
- 6 in a row.
- On contact chain reaction happens and breaks the adjacent bricks(diagonally, vertically and horizontally)

## OOPS
#### Inheritance
Inheritance allows us to define a class that inherits all the methods and properties from another class.
- **Parent**
```
class Bricks:
    def __init__(self):
        self.bricks = "X"
        self.strength = 0

    def strength(self):
        return self.strength
```
- **Child**
```
class Brick(Bricks):
    def __init__(self):
        super().__init__()
        self.strength = 1

    def strength(self):
        return self.strength
```
#### Polymorphism
Polymorphism allows us to define methods in the child class with the same name as defined in their parent class.
```
class Powerup:

    def disappear(self):
        print("Parent Disappear. So exiting........")
        quit()

    def reappear(self):
        print("Parent Deactivate. So exiting........")
        quit()
```
Every powerup mentioned above has these 2 functions as these 2 functions help powerup move.
```
class Expand(Powerup):
    
    def starting_position(self, grid, x, y):
        grid[self.x][self.y] = self.shape
    
    def disappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = " "
    
    def reappear(self, obj_board):
        obj_board.matrix[self.x][self.y] = self.shape
```
#### Encapsulation
The idea of wrapping data and the methods that work on data within one unit. Prevents accidental modification of data. One example is:
```
class Props:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

class Ball(Props):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.shape = "o"

class Paddle(Props):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.shape = ["I", "I", "I", "I", "I", "I", "I"]
```

#### Abstraction
Abstraction means hiding the complexity and only showing the essential features of the object. Some of the examples are:
```
class Paddle(Props):
    
    def get_len(self):
        return len(self.shape)

def move():
	x = obj_ball.get_x()
	y = obj_ball.get_y()
	vel_x = obj_ball.get_velx()
	vel_y = obj_ball.get_vely()
	obj_ball.disappear_ball(obj_board)
	obj_ball.x+=vel_x
	obj_ball.y+=vel_y
	obj_ball.reappear_ball(obj_board)
```
- get_len() is abstraction
- move() is abstraction too.