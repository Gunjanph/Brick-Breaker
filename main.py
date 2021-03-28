import signal
import os
import time
from random import randrange, randint
import numpy as np
from colorama import init, Fore, Back
init()

from input import Get, input_to
from board import Board
from paddle import Paddle
from ball import Ball
from bricks import Brick, UnbreakableBrick
from config import Config
from explode  import Explode
from powerup import Powerup
from expand import Expand
from shrink import Shrink
from fast import Fast
from grab import Grab
from thru import Thru

obj_board = Board(30,110)
obj_board.create_board()

obj_paddle = Paddle(28,47,1)
obj_paddle.starting_position(obj_board.matrix)

ball_y = randrange(47,53)
# ball_y = 50
obj_ball = Ball(27,ball_y,1)
obj_ball.starting_position(obj_board.matrix)

obj_brick = Brick()
obj_brick.appear_brick(obj_board.matrix)

# obj_brick2 = Brick2()
# obj_brick2.appear_brick2(obj_board.matrix)

# obj_brick3 = Brick3()
# obj_brick3.appear_brick3(obj_board.matrix)

obj_unbrick = UnbreakableBrick()
obj_unbrick.appear_unb(obj_board.matrix)

obj_explode = Explode()
obj_explode.exappear_brick(obj_board.matrix)

# obj_powerup = Powerup()
powerup_list = []
active_powerup = []

obj_config = Config()

get = Get()

obj_ball.vely = 0

def find_line(point1, point2):
	return np.cross(list(point1)+[1], list(point2)+[1])

# point1 = (0,0)
# point2 = (2,3)
# point2 = (0,4)

def find_points(point1, point2):
	a,b,c = find_line(point1,point2)
	# print(a,b,c)
	x1,y1 = point1
	x2,y2 = point2
	xv = 2*(x1<x2)-1
	yv = 2*(y1<y2)-1
	points = []
	if abs(x1-x2) > abs(y1-y2):
		for x in range(x1,x2+xv,xv):
			y = -(a*x + c)/b
			points.append((x,int(y)))
			if(y - int(y) != 0):
				points.append((x,int(y)+1))
	else:
		for y in range(y1,y2+yv,yv):
			x = -(b*y + c)/a
			points.append((int(x),y))
			if(x - int(x) != 0):
				points.append((int(x)+1,y))

	points.sort(key = lambda x: x[0], reverse=(xv==-1))
	return points
# points = find_points(point1, point2, 1)
# print(points)

def reposition():
	obj_ball.y = randrange(47,53)
	# obj_ball.y = 50
	obj_paddle.y = 47
	obj_paddle.x = 28
	obj_ball.x = 27
	obj_ball.number = 1
	obj_ball.vely = 0
	obj_ball.velx = 0
	obj_paddle.starting_position(obj_board.matrix)
	obj_ball.starting_position(obj_board.matrix)
	for i in range(len(active_powerup)):
		if active_powerup[i][0].number == 1:
			obj_paddle.disappear_paddle(obj_board)
			obj_paddle.expand()
			obj_paddle.reappear_paddle(obj_board)
		if active_powerup[i][0].number == 2:
			obj_paddle.disappear_paddle(obj_board)
			obj_paddle.shrink()
			obj_paddle.reappear_paddle(obj_board)
		if active_powerup[i][0].number == 3:
			if obj_ball.velx < 0 and obj_ball.velx >= -1:
				obj_ball.velx += 1
			if obj_ball.velx > 0 and obj_ball.velx <= 1:
				obj_ball.velx -= 1
		if active_powerup[i][0].number == 4:
			obj_ball.active = 0
		if active_powerup[i][0].number == 5:
			obj_ball.thruactive = 0
	active_powerup.clear()

def powup(numb, x, y):
	if numb == 1:
		# quit()
		obj_shrink = Shrink(x, y)
		obj_shrink.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_shrink)
	
	elif numb == 2:
		# quit()
		obj_expand = Expand(x, y)
		obj_expand.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_expand)

	elif numb == 3:
		# quit()
		obj_fast = Fast(x, y)
		obj_fast.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_fast)

	elif numb == 4:
		obj_grab = Grab(x, y)
		obj_grab.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_grab)
	
	elif numb == 5:
		obj_thru = Thru(x, y)
		obj_thru.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_thru)

def movepowerup():
	for i in range(len(powerup_list)):
		if powerup_list[i].x + powerup_list[i].velx < 28:
			powerup_list[i].disappear(obj_board)
			powerup_list[i].x += powerup_list[i].velx
			powerup_list[i].reappear(obj_board)
		else:
			powerup_list[i].disappear(obj_board)
			powerup_list.pop(i)

def endpowerup():
	for i in range(len(active_powerup)):
		if(time.time()-active_powerup[i][1] >= active_powerup[i][0].time):
			if active_powerup[i][0].number == 1:
				obj_paddle.disappear_paddle(obj_board)
				obj_paddle.expand()
				obj_paddle.reappear_paddle(obj_board)
			if active_powerup[i][0].number == 2:
				obj_paddle.disappear_paddle(obj_board)
				obj_paddle.shrink()
				obj_paddle.reappear_paddle(obj_board)
			if active_powerup[i][0].number == 3:
				if obj_ball.velx < 0 and obj_ball.velx >= -1:
					obj_ball.velx += 1
				if obj_ball.velx > 0 and obj_ball.velx <= 1:
					obj_ball.velx -= 1
			if active_powerup[i][0].number == 4:
				obj_ball.active = 0
			if active_powerup[i][0].number == 5:
				obj_ball.thruactive = 0
			active_powerup.pop(i)
			break;

def movepaddle():
	char = input_to(get)
	# print(char)
	bx = obj_ball.get_x()
	bay = obj_ball.get_y()
	by = obj_ball.get_velx()
	vely = obj_ball.get_vely()
	py = obj_paddle.get_y()
	length = obj_paddle.get_len()

	if char == 'q':
		print("QUIT :(")
		quit()
	
	if char == 'd':
		move_right = obj_paddle.right_collision(bx, by)
		# print(bx, by)
		
		if(move_right == 2):
			# obj_ball.direction = 1
			# obj_ball.disappear_ball(obj_board)
			# obj_ball.y+=1
			# obj_ball.reappear_ball(obj_board)
			obj_paddle.direction = 1
			obj_paddle.disappear_paddle(obj_board)
			obj_paddle.y+=2
			obj_paddle.reappear_paddle(obj_board)
			# print(obj_paddle.y)
		
		if(move_right == 1):
			obj_ball.direction = 1
			obj_ball.disappear_ball(obj_board)
			obj_ball.y+=2
			obj_ball.reappear_ball(obj_board)
			obj_paddle.direction = 1
			obj_paddle.disappear_paddle(obj_board)
			obj_paddle.y+=2
			obj_paddle.reappear_paddle(obj_board)
			# print(obj_paddle.y)
	
	if char == 'a':
		move_left = obj_paddle.left_collision(bx, by)
		
		if(move_left == 2):
			obj_paddle.direction = -1
			obj_paddle.disappear_paddle(obj_board)
			obj_paddle.y-=2
			obj_paddle.reappear_paddle(obj_board)
			# print(obj_paddle.y)
		
		if(move_left == 1):
			obj_paddle.direction = -1
			obj_ball.direction = -1
			obj_paddle.disappear_paddle(obj_board)
			obj_ball.disappear_ball(obj_board)
			obj_paddle.y-=2
			obj_ball.y-=2
			obj_paddle.reappear_paddle(obj_board)
			obj_ball.reappear_ball(obj_board)

	if char == ' ':
		obj_ball.velx = -1
		obj_ball.vely = vely + (bay - (py + (int)(length/2)))

def move():
	x = obj_ball.get_x()
	y = obj_ball.get_y()
	vel_x = obj_ball.get_velx()
	vel_y = obj_ball.get_vely()
	obj_ball.disappear_ball(obj_board)
	obj_ball.x+=vel_x
	obj_ball.y+=vel_y
	obj_ball.reappear_ball(obj_board)

def collision():
	# obj_ball.vely = 1
	x = obj_ball.get_x()
	y = obj_ball.get_y()
	py = obj_paddle.get_y()
	length = obj_paddle.get_len()
	vel_x = obj_ball.get_velx()
	vel_y = obj_ball.get_vely()
	powerupnumber = 0
	# wall
	if x <= 1:
		obj_ball.velx = -vel_x
	
	if x >= 28:
		obj_ball.number-=1
		
		if obj_ball.number == 0:
			obj_config.life-=1
	
			if obj_config.life == 0:
				print("GAME OVER")
				quit()
			else:
				obj_ball.disappear_ball(obj_board)
				obj_paddle.disappear_paddle(obj_board)
				reposition()

	if y+vel_y >= 109 or y <= 0:
		obj_ball.vely = -vel_y
	
	# paddle
	if x+vel_x<=29 and y+vel_y<=109:
		if obj_board.matrix[x+1][y] == "I":
			if vel_x!=0 or vel_y!=0:
				# quit()
				if obj_ball.active == 1:
					# quit()
					obj_ball.vely = 0
					obj_ball.velx = 0
				else:
					obj_ball.vely = vel_y + (y - (py + (int)(length/2)))
					obj_ball.velx = -vel_x
	for i in range(len(powerup_list)):
		if powerup_list[i].x+2 <= 29:
			if obj_board.matrix[powerup_list[i].x+2][powerup_list[i].y] == "I" or obj_board.matrix[powerup_list[i].x+1][powerup_list[i].y] == "I":
				# quit()
				# active_powerup.append((powerup_list[i], time.time()))
				powerup_list[i].disappear(obj_board)
				if powerup_list[i].number == 1:
					# quit()
					if obj_paddle.get_len() > 3:
						obj_paddle.disappear_paddle(obj_board)
						obj_paddle.shrink()
						obj_paddle.reappear_paddle(obj_board)
						active_powerup.append((powerup_list[i], time.time()))
				if powerup_list[i].number == 2:
					# quit()
					if obj_paddle.get_len() < 9:
						obj_paddle.disappear_paddle(obj_board)
						obj_paddle.expand()
						obj_paddle.reappear_paddle(obj_board)
						active_powerup.append((powerup_list[i], time.time()))
				if powerup_list[i].number == 3:
					# quit()
					active_powerup.append((powerup_list[i], time.time()))
					if obj_ball.velx < 0 and obj_ball.velx >= -1:
						obj_ball.velx -= 1
					if obj_ball.velx > 0 and obj_ball.velx <= 1:
						obj_ball.velx += 1
				if powerup_list[i].number == 4:
					# quit()
					active_powerup.append((powerup_list[i], time.time()))
					obj_ball.active = 1
				if powerup_list[i].number == 5:
					active_powerup.append((powerup_list[i], time.time()))
					obj_ball.thruactive = 1
				powerup_list.pop(i)
				break;

	# brick
	point1 = (x,y)
	point2 = (x+vel_x,y+vel_y)
	if vel_x!=0 or vel_y!=0:
		pts = find_points(point1, point2)
		# print(pts)
		if vel_y==0:
			for i in range(len(pts)):
				if pts[i][1]<=109 and pts[i][0]<=29:
					if obj_board.matrix[pts[i][0]][pts[i][1]] == "X":
						if obj_board.matrix[pts[i][0]][pts[i][1]+1] == -10:
							obj_explode.exdisappear_brick(obj_board,pts[i][0],pts[i][1],obj_config)
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
						else:
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
								powerupnumber = obj_brick.disappear_brick(obj_board,pts[i][0],pts[i][1],obj_config)
								powup(powerupnumber, pts[i][0], pts[i][1])
							else:
								obj_config.score += obj_board.matrix[pts[i][0]][pts[i][1]+1]
						break;
					if obj_board.matrix[pts[i][0]][pts[i][1]-1] == "X":
						if obj_board.matrix[pts[i][0]][pts[i][1]] == -10:
							obj_explode.exdisappear_brick(obj_board,pts[i][0],pts[i][1]-1,obj_config)
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
						else:
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
								powerupnumber = obj_brick.disappear_brick(obj_board,pts[i][0],pts[i][1]-1,obj_config)
								powup(powerupnumber, pts[i][0], pts[i][1])
							else:
								obj_config.score += obj_board.matrix[pts[i][0]][pts[i][1]]
						break;
					if obj_board.matrix[pts[i][0]][pts[i][1]+1] == "X":
						if obj_board.matrix[pts[i][0]][pts[i][1]+2] == -10:
							obj_explode.exdisappear_brick(obj_board,pts[i][0],pts[i][1]+1,obj_config)
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
						else:
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
								powerupnumber = obj_brick.disappear_brick(obj_board,pts[i][0],pts[i][1]+1,obj_config)
								powup(powerupnumber, pts[i][0], pts[i][1])
							else:
								obj_config.score += obj_board.matrix[pts[i][0]][pts[i][1]+2]
						break;
		else:
			for i in range(len(pts)):
				if pts[i][1]<=109 and pts[i][0]<=29:
					if obj_board.matrix[pts[i][0]][pts[i][1]] == "X":
						if obj_board.matrix[pts[i][0]][pts[i][1]+1] == -10:
							obj_explode.exdisappear_brick(obj_board,pts[i][0],pts[i][1],obj_config)
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
						else:
							if obj_ball.thruactive == 0:
								obj_ball.velx = -vel_x
								powerupnumber = obj_brick.disappear_brick(obj_board,pts[i][0],pts[i][1],obj_config)
								powup(powerupnumber, pts[i][0], pts[i][1])
							else:
								obj_config.score += obj_board.matrix[pts[i][0]][pts[i][1]+1]
						# if (vel_x<0 and vel_y<0) or (vel_x>0 and vel_y>0):
						# 	obj_ball.velx = -vel_x
						# else:
						# 	obj_ball.vely = -vel_y
						break;
	
x=time.time()
y=x
z=x
count = 0

# collision()

while True:
	os.system('clear')
	obj_config.time = (round(time.time()) - round(x))
	string = "SCORE: " + str(obj_config.score) + " | LIVES: " + str(obj_config.life) + " | TIME PLAYED: " + str(obj_config.time)
	if obj_config.time >= 150:
		print("TIME OUT")
		quit()
	# obj_board.theyllprintit(string)
	temp = obj_board.theyllprintit(string)
	if temp == 0:
		print("YOU WON :)")
		quit()
	# movepaddle()
	# if time.time() - y >= 0.3:
	# 	y = time.time()
	movepaddle()
	move()
	collision()
	movepowerup()
	endpowerup()
	# 	move() # move is clearing the last block
	# count += 1
	# time.sleep(0.10)