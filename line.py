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