import signal
import os
import time
import subprocess
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
from bullet import Bullet
from bullets import Bullets
from falling import Falling_Brick
from rainbow import Rainbow_Brick
from boss import Boss
from bomb import Bomb

obj_board = Board(30,110)
obj_board.create_board()

obj_config = Config()

row = 1 #how much fall the brick
flag = 0
rainbow_flag = 0
health_flag = 0


obj_paddle = Paddle(28,47,1)
obj_paddle.starting_position(obj_board.matrix)

ball_y = randrange(47,53)

obj_ball = Ball(27,ball_y,1)
obj_ball.starting_position(obj_board.matrix)

obj_brick = Brick()
obj_brick.appear_brick(obj_board.matrix, 1, 0)

obj_unbrick = UnbreakableBrick()
obj_unbrick.appear_unb(obj_board.matrix,1)

obj_explode = Explode()
obj_explode.exappear_brick(obj_board.matrix, obj_config.level)

obj_fall = Falling_Brick()

obj_rainbow = Rainbow_Brick()
obj_rainbow.rainbow_appear_brick(obj_board)

obj_boss = Boss(2, 31, 1)

powerup_list = []
start_powerup = []
active_powerup = []
brick_flag = []
laser = []
bombs = []

get = Get()

obj_ball.vely = 0

def find_line(point1, point2):
	return np.cross(list(point1)+[1], list(point2)+[1])

def find_points(point1, point2):
	a,b,c = find_line(point1,point2)
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

def reposition():
	obj_ball.y = 50
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
		if active_powerup[i][0].number == 6:
				obj_config.bullet = 0
	active_powerup.clear()

def powup(numb, x, y):
	if numb == 1:
		obj_shrink = Shrink(x, y)
		obj_shrink.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_shrink)
		start_powerup.append(obj_shrink)
	
	elif numb == 2:
		obj_expand = Expand(x, y)
		obj_expand.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_expand)
		start_powerup.append(obj_expand)

	elif numb == 3:
		obj_fast = Fast(x, y)
		obj_fast.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_fast)
		start_powerup.append(obj_fast)

	elif numb == 4:
		obj_grab = Grab(x, y)
		obj_grab.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_grab)
		start_powerup.append(obj_grab)
	
	elif numb == 5:
		obj_thru = Thru(x, y)
		obj_thru.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_thru)
		start_powerup.append(obj_thru)

	elif numb == 6:
		obj_bullet = Bullet(x, y)
		obj_bullet.starting_position(obj_board.matrix, x, y)
		powerup_list.append(obj_bullet)
		start_powerup.append(obj_bullet)

def impartpowerup():
	for i in range(len(start_powerup)):
		start_powerup[i].disappear(obj_board)
		if obj_ball.velx>0:
			start_powerup[i].x = 0
		else:
			start_powerup[i].x-=obj_ball.velx
		start_powerup[i].y+=obj_ball.vely
		start_powerup[i].vely = obj_ball.vely
		if obj_board.matrix[start_powerup[i].x][start_powerup[i].y] == "X" or isinstance(obj_board.matrix[start_powerup[i].x][start_powerup[i].y], int)==True:
			print("in if")
			brick_flag.append((start_powerup[i].x,start_powerup[i].y, obj_board.matrix[start_powerup[i].x][start_powerup[i].y]))
		start_powerup[i].reappear(obj_board)
		start_powerup.pop(i)

def movepowerup():
	for i in range(len(powerup_list)):
		if powerup_list[i].x + powerup_list[i].velx < 28:
			if powerup_list[i].y + powerup_list[i].vely >= 109 or powerup_list[i].y + powerup_list[i].vely <= 0:
				powerup_list[i].vely = -powerup_list[i].vely
			if powerup_list[i].x + powerup_list[i].velx <= 0:
				powerup_list[i].velx = -powerup_list[i].velx
			powerup_list[i].disappear(obj_board)
			for j in range(len(brick_flag)):
				if brick_flag[j][0] == powerup_list[i].x and brick_flag[j][1] == powerup_list[i].y:
					print("in loop")
					obj_board.matrix[powerup_list[i].x][powerup_list[i].y] = brick_flag[j][2]
					brick_flag.pop(j)
			powerup_list[i].x += powerup_list[i].velx
			powerup_list[i].y += powerup_list[i].vely
			if obj_board.matrix[powerup_list[i].x][powerup_list[i].y] == "X" or isinstance(obj_board.matrix[powerup_list[i].x][powerup_list[i].y], int)==True:
				brick_flag.append((powerup_list[i].x,powerup_list[i].y, obj_board.matrix[powerup_list[i].x][powerup_list[i].y]))
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
			if active_powerup[i][0].number == 6:
				obj_config.bullet = 0
			active_powerup.pop(i)
			break;
		else:
			if active_powerup[i][0].number == 6:
				return 10 - round(time.time())+round(active_powerup[i][1])

def shoot():
	x = 27
	y = obj_paddle.y+1
	obj_bullets = Bullets(x,y,1)
	obj_bullets.starting_position(obj_board.matrix, x, y)
	laser.append(obj_bullets)

def bossbomb():
	x = obj_boss.x+8
	y = obj_boss.y+19
	obj_bomb = Bomb(x,y,1)
	obj_bomb.starting_position(obj_board.matrix, x, y)
	bombs.append(obj_bomb)

def movepaddle():
	char = input_to(get)
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
		
		if(move_right == 2):
			if obj_config.level == 1 or obj_config.level == 2:
				obj_paddle.direction = 1
				obj_paddle.disappear_paddle(obj_board)
				obj_paddle.y+=2
				obj_paddle.reappear_paddle(obj_board)
			if obj_config.level == 3:
				if obj_paddle.y<92:
					obj_paddle.direction = 1
					obj_paddle.disappear_paddle(obj_board)
					obj_paddle.y+=2
					obj_paddle.reappear_paddle(obj_board)
				if(obj_boss.y+39 <= 107):
					obj_boss.disappear_boss(obj_board)
					obj_boss.y += 2
					obj_boss.appear_boss(obj_board)
		
		if(move_right == 1):
			if obj_config.level == 1 or obj_config.level == 2:
				obj_ball.direction = 1
				obj_ball.disappear_ball(obj_board)
				obj_ball.y+=2
				obj_ball.reappear_ball(obj_board)
				obj_paddle.direction = 1
				obj_paddle.disappear_paddle(obj_board)
				obj_paddle.y+=2
				obj_paddle.reappear_paddle(obj_board)
			if obj_config.level == 3:
				if obj_paddle.y<95:
					obj_ball.direction = 1
					obj_ball.disappear_ball(obj_board)
					obj_ball.y+=2
					obj_ball.reappear_ball(obj_board)
					obj_paddle.direction = 1
					obj_paddle.disappear_paddle(obj_board)
					obj_paddle.y+=2
					obj_paddle.reappear_paddle(obj_board)
		
				if(obj_boss.y+39 <= 107):
					obj_boss.disappear_boss(obj_board)
					obj_boss.y += 2
					obj_boss.appear_boss(obj_board)

	
	if char == 'a':
		move_left = obj_paddle.left_collision(bx, by)
		
		if(move_left == 2):
			if obj_config.level == 1 or obj_config.level == 2:
				obj_paddle.direction = -1
				obj_paddle.disappear_paddle(obj_board)
				obj_paddle.y-=2
				obj_paddle.reappear_paddle(obj_board)
			if obj_config.level == 3:
				if obj_paddle.y<90:
					obj_paddle.direction = -1
					obj_paddle.disappear_paddle(obj_board)
					obj_paddle.y-=2
					obj_paddle.reappear_paddle(obj_board)
				if(obj_boss.y >= 2):
					obj_boss.disappear_boss(obj_board)
					obj_boss.y -= 2
					obj_boss.appear_boss(obj_board)
		
		if(move_left == 1):
			if obj_config.level == 1 or obj_config.level == 2:
				obj_paddle.direction = -1
				obj_ball.direction = -1
				obj_paddle.disappear_paddle(obj_board)
				obj_ball.disappear_ball(obj_board)
				obj_paddle.y-=2
				obj_ball.y-=2
				obj_paddle.reappear_paddle(obj_board)
				obj_ball.reappear_ball(obj_board)
			if obj_config.level == 3:
				if obj_paddle.y>18:
					obj_paddle.direction = -1
					obj_ball.direction = -1
					obj_paddle.disappear_paddle(obj_board)
					obj_ball.disappear_ball(obj_board)
					obj_paddle.y-=2
					obj_ball.y-=2
					obj_paddle.reappear_paddle(obj_board)
					obj_ball.reappear_ball(obj_board)

				if(obj_boss.y >= 2):
					obj_boss.disappear_boss(obj_board)
					obj_boss.y -= 2
					obj_boss.appear_boss(obj_board)

	if char == 'l':
		obj_config.level += 1
		obj_config.start_time[obj_config.level-1] = obj_config.time
		obj_brick.level_disappear_brick(obj_board)
		obj_brick.appear_brick(obj_board.matrix, obj_config.level, health_flag)
		obj_unbrick.appear_unb(obj_board.matrix, obj_config.level)
		obj_explode.exappear_brick(obj_board.matrix, obj_config.level)
		obj_ball.disappear_ball(obj_board)
		obj_paddle.disappear_paddle(obj_board)
		reposition()
		if obj_config.level == 3:
			obj_boss.starting_position(obj_board.matrix)

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
	global rainbow_flag
	x = obj_ball.get_x()
	y = obj_ball.get_y()
	py = obj_paddle.get_y()
	length = obj_paddle.get_len()
	vel_x = obj_ball.get_velx()
	vel_y = obj_ball.get_vely()
	powerupnumber = 0
	
	# paddle
	if x+vel_x<=29 and y+vel_y<=109:
		if obj_board.matrix[x+1][y] == "I" or (vel_x==2 and obj_board.matrix[x+2][y] == "I"):
			if vel_x!=0 or vel_y!=0:
				subprocess.Popen(['aplay', './sound/mb_hit.wav'])
				os.system('clear')
				if flag == 1:
					obj_fall.fall_appear_brick(obj_board)
				if obj_ball.active == 1:
					obj_ball.vely = 0
					obj_ball.velx = 0
				else:
					obj_ball.vely = vel_y + (y - (py + (int)(length/2)))
					obj_ball.velx = -vel_x
	for i in range(len(powerup_list)):
		if powerup_list[i].x+2 <= 29:
			if obj_board.matrix[powerup_list[i].x+2][powerup_list[i].y] == "I" or obj_board.matrix[powerup_list[i].x+1][powerup_list[i].y] == "I":
				powerup_list[i].disappear(obj_board)
				if powerup_list[i].number == 1:
					if obj_paddle.get_len() > 3:
						obj_paddle.disappear_paddle(obj_board)
						obj_paddle.shrink()
						obj_paddle.reappear_paddle(obj_board)
						active_powerup.append((powerup_list[i], time.time()))
				if powerup_list[i].number == 2:
					if obj_paddle.get_len() < 9:
						obj_paddle.disappear_paddle(obj_board)
						obj_paddle.expand()
						obj_paddle.reappear_paddle(obj_board)
						active_powerup.append((powerup_list[i], time.time()))
				if powerup_list[i].number == 3:
					active_powerup.append((powerup_list[i], time.time()))
					if obj_ball.velx < 0 and obj_ball.velx >= -1:
						obj_ball.velx -= 1
					if obj_ball.velx > 0 and obj_ball.velx <= 1:
						obj_ball.velx += 1
				if powerup_list[i].number == 4:
					active_powerup.append((powerup_list[i], time.time()))
					obj_ball.active = 1
				if powerup_list[i].number == 5:
					active_powerup.append((powerup_list[i], time.time()))
					obj_ball.thruactive = 1
				if powerup_list[i].number == 6:
					active_powerup.append((powerup_list[i], time.time()))
					obj_config.bullet = 1
				subprocess.Popen(['aplay', './sound/mb_hit.wav'])
				os.system('clear')
				powerup_list.pop(i)
				break;
	
	# wall
	if x <= 1:
		obj_ball.velx = -vel_x
		subprocess.Popen(['aplay', './sound/mb_wall.wav'])
		os.system('clear')
	
	if x >= 28:
		obj_ball.number-=1
		
		if obj_ball.number == 0:
			obj_config.life-=1
	
			if obj_config.life == 0:
				print("GAME OVER")
				subprocess.Popen(['aplay', './sound/mb_die.wav'])
				os.system('clear')
				quit()
			else:
				obj_ball.disappear_ball(obj_board)
				obj_paddle.disappear_paddle(obj_board)
				reposition()
				subprocess.Popen(['aplay', './sound/mb_wall.wav'])
				os.system('clear')

	if y+vel_y >= 109 or y <= 0:
		obj_ball.vely = -vel_y
		subprocess.Popen(['aplay', './sound/mb_wall.wav'])
		os.system('clear')

	# brick
	point1 = (x,y)
	point2 = (x+vel_x,y+vel_y)
	if vel_x!=0 or vel_y!=0:
		pts = find_points(point1, point2)
		if vel_y==0:
			for i in range(len(pts)):
				if pts[i][1]<=109 and pts[i][0]<=29:
					if obj_board.matrix[pts[i][0]][pts[i][1]] == "X":
						if pts[i][0] == 6 and pts[i][1] == 20:
							rainbow_flag = 1
						if obj_board.matrix[pts[i][0]][pts[i][1]+1] == -10:
							subprocess.Popen(['aplay', './sound/mb_brick.wav'])
							os.system('clear')
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
					elif obj_board.matrix[pts[i][0]][pts[i][1]-1] == "X":
						if pts[i][0] == 6 and pts[i][1]-1 == 20:
							rainbow_flag = 1
						if obj_board.matrix[pts[i][0]][pts[i][1]] == -10:
							subprocess.Popen(['aplay', './sound/mb_brick.wav'])
							os.system('clear')
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
					elif obj_board.matrix[pts[i][0]][pts[i][1]+1] == "X":
						if pts[i][0] == 6 and pts[i][1]+1 == 20:
							rainbow_flag = 1
						if obj_board.matrix[pts[i][0]][pts[i][1]+2] == -10:
							subprocess.Popen(['aplay', './sound/mb_brick.wav'])
							os.system('clear')
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
					elif obj_board.matrix[pts[i][0]][pts[i][1]] == "-" or obj_board.matrix[pts[i][0]][pts[i][1]] == "=" or obj_board.matrix[pts[i][0]][pts[i][1]] == ":" or obj_board.matrix[pts[i][0]][pts[i][1]] == "(" or obj_board.matrix[pts[i][0]][pts[i][1]] == ")" or obj_board.matrix[pts[i][0]][pts[i][1]] == "*" or obj_board.matrix[pts[i][0]][pts[i][1]] == "`" or obj_board.matrix[pts[i][0]][pts[i][1]] == ".":
						obj_ball.velx = -vel_x
						obj_ball.disappear_ball(obj_board)
						obj_ball.reappear_ball(obj_board)
						obj_boss.health -= 10
						break;
					elif obj_board.matrix[pts[i][0]][pts[i][1]-1] == "-" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "=" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == ":" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "(" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == ")" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "*" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "`" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == ".":
						obj_ball.velx = -vel_x
						obj_ball.disappear_ball(obj_board)
						obj_ball.reappear_ball(obj_board)
						obj_boss.health -= 10
						break;
					elif obj_board.matrix[pts[i][0]][pts[i][1]+1] == "-" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "=" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == ":" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "(" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == ")" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "*" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "`" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == ".":
						obj_ball.velx = -vel_x
						obj_ball.disappear_ball(obj_board)
						obj_ball.reappear_ball(obj_board)
						obj_boss.health -= 10
						break;
		else:
			for i in range(len(pts)):
				if pts[i][1]<=109 and pts[i][0]<=29:
					if obj_board.matrix[pts[i][0]][pts[i][1]] == "X":
						if obj_board.matrix[pts[i][0]][pts[i][1]+1] == -10:
							subprocess.Popen(['aplay', './sound/mb_brick.wav'])
							os.system('clear')
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
					elif obj_board.matrix[pts[i][0]][pts[i][1]] == "-" or obj_board.matrix[pts[i][0]][pts[i][1]] == "=" or obj_board.matrix[pts[i][0]][pts[i][1]] == ":" or obj_board.matrix[pts[i][0]][pts[i][1]] == "(" or obj_board.matrix[pts[i][0]][pts[i][1]] == ")" or obj_board.matrix[pts[i][0]][pts[i][1]] == "*" or obj_board.matrix[pts[i][0]][pts[i][1]] == "`" or obj_board.matrix[pts[i][0]][pts[i][1]] == ".":
						obj_ball.velx = -vel_x
						obj_ball.disappear_ball(obj_board)
						obj_ball.reappear_ball(obj_board)
						obj_boss.health -= 10
						break;
					elif obj_board.matrix[pts[i][0]][pts[i][1]-1] == "-" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "=" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == ":" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "(" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == ")" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "*" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == "`" or obj_board.matrix[pts[i][0]][pts[i][1]-1] == ".":
						obj_ball.velx = -vel_x
						obj_ball.disappear_ball(obj_board)
						obj_ball.reappear_ball(obj_board)
						obj_boss.health -= 10
						break;
					elif obj_board.matrix[pts[i][0]][pts[i][1]+1] == "-" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "=" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == ":" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "(" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == ")" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "*" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == "`" or obj_board.matrix[pts[i][0]][pts[i][1]+1] == ".":
						obj_ball.velx = -vel_x
						obj_ball.disappear_ball(obj_board)
						obj_ball.reappear_ball(obj_board)
						obj_boss.health -= 10
						break;
		#bullet brick
		i=0
		while i < len(laser):
			if laser[i].x+laser[i].velx<=1:
				laser[i].disappear(obj_board)
				laser.pop(i)
			elif obj_board.matrix[laser[i].x+laser[i].velx][laser[i].y] == "X":
				if obj_board.matrix[laser[i].x+laser[i].velx][laser[i].y+1] == -10:
					subprocess.Popen(['aplay', './sound/mb_brick.wav'])
					os.system('clear')
					obj_explode.exdisappear_brick(obj_board,laser[i].x+laser[i].velx,laser[i].y,obj_config)
				else:
					powerupnumber = obj_brick.disappear_brick(obj_board, laser[i].x+laser[i].velx, laser[i].y, obj_config)
					powup(powerupnumber, laser[i].x, laser[i].y)
				laser[i].disappear(obj_board)
				laser.pop(i)
			elif isinstance(obj_board.matrix[laser[i].x][laser[i].y], int)==True:
				temp = obj_board.matrix[laser[i].x][laser[i].y]
				laser[i].disappear(obj_board)
				obj_board.matrix[laser[i].x][laser[i].y] = temp
				laser[i].x = laser[i].x+laser[i].velx
				laser[i].reappear(obj_board)

			else:
				laser[i].disappear(obj_board)
				laser[i].x = laser[i].x+laser[i].velx
				laser[i].reappear(obj_board)
			i+=1

		# bomb
		i=0
		while i < len(bombs):
			if bombs[i].x+bombs[i].velx>28:
				bombs[i].disappear(obj_board)
				bombs.pop(i)
			elif obj_board.matrix[bombs[i].x+bombs[i].velx][bombs[i].y] == "X":
				if obj_board.matrix[bombs[i].x+bombs[i].velx][bombs[i].y+1] == -10:
					subprocess.Popen(['aplay', './sound/mb_brick.wav'])
					os.system('clear')
					obj_explode.exdisappear_brick(obj_board,bombs[i].x+bombs[i].velx,bombs[i].y,obj_config)
				else:
					powerupnumber = obj_brick.disappear_brick(obj_board, bombs[i].x+bombs[i].velx, bombs[i].y, obj_config)
					powup(powerupnumber, bombs[i].x, bombs[i].y)
				bombs[i].disappear(obj_board)
				bombs.pop(i)
			elif isinstance(obj_board.matrix[bombs[i].x][bombs[i].y], int)==True:
				temp = obj_board.matrix[bombs[i].x][bombs[i].y]
				bombs[i].disappear(obj_board)
				obj_board.matrix[bombs[i].x][bombs[i].y] = temp
				bombs[i].x = bombs[i].x+bombs[i].velx
				bombs[i].reappear(obj_board)
			elif obj_board.matrix[bombs[i].x+bombs[i].velx][bombs[i].y] == "I":
				obj_config.life -= 1
				if obj_config.life == 0:
					print("GAME OVER")
					subprocess.Popen(['aplay', './sound/mb_die.wav'])
					os.system('clear')
					quit()
				bombs[i].disappear(obj_board)
				bombs.pop(i)
			else:
				bombs[i].disappear(obj_board)
				bombs[i].x = bombs[i].x+bombs[i].velx
				bombs[i].reappear(obj_board)
			i+=1


x=time.time()
y=x
z=x
count = 0
time_bullet = 10

while True:
	os.system('clear')
	obj_config.time = (round(time.time()) - round(x))
	if obj_config.bullet==1:
		string = "SCORE: " + str(obj_config.score) + " | LIVES: " + str(obj_config.life) + " | TIME PLAYED: " + str(obj_config.time) + " | LEVEL:" + str(obj_config.level) + " | TIME REMAINING:" + str(time_bullet)
	else:
		string = "SCORE: " + str(obj_config.score) + " | LIVES: " + str(obj_config.life) + " | TIME PLAYED: " + str(obj_config.time) + " | LEVEL:" + str(obj_config.level)

	if obj_config.time-obj_config.start_time[obj_config.level-1] >= 60:
		flag = 1
	else:
		flag = 0

	if obj_boss.health == 50:
		health_flag = 1
		obj_brick.appear_brick(obj_board.matrix, obj_config.level, health_flag)

	if obj_boss.health == 20:
		obj_brick.appear_brick(obj_board.matrix, obj_config.level, health_flag)

	temp = obj_board.theyllprintit(string, obj_config.bullet, obj_config.level, obj_boss.health)
	if temp == 0:
		if obj_config.level!=3:
			obj_config.level += 1
			obj_config.start_time[obj_config.level-1] = obj_config.time
			obj_brick.level_disappear_brick(obj_board)
			obj_brick.appear_brick(obj_board.matrix, obj_config.level, health_flag)
			obj_unbrick.appear_unb(obj_board.matrix, obj_config.level)
			obj_explode.exappear_brick(obj_board.matrix, obj_config.level)
			obj_ball.disappear_ball(obj_board)
			obj_paddle.disappear_paddle(obj_board)
			reposition()

		if obj_config.level == 3:
			obj_boss.starting_position(obj_board.matrix)
			if time.time() - y >= 0.5:
				y = time.time()
				bossbomb()
	movepaddle()
	move()
	if obj_config.bullet==1:
		if time.time() - y >= 0.5:
			y = time.time()
			shoot()
	collision()
	impartpowerup()
	movepowerup()
	time_bullet = endpowerup()
	if rainbow_flag == 0 and obj_config.level == 1:
		obj_rainbow.color(obj_board)