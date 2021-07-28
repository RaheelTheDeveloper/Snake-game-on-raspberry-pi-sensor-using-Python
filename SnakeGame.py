
from sense_hat import SenseHat
import time
from time import sleep
from random import randint

sense = SenseHat()

snake = [[1,2],[2,2],[3,2]]
white = (255,255,255)
direction = "right"
SnakeDirection = (1,0)
blank = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
foodToEat = []
scorePoint = 0
speed = 0.5
SnakeIsDead = False
DL = "hi"

acceleration = []
x = 0
y = 0
z = 0

right = (1,0)
left = (-1,0)
up = (0,-1)
down = (0,1)

sense.clear()

def Draw_Snake():
	for segment in snake:
		sense.set_pixel(segment[0], segment[1], white)

def Move():
	global scorePoint
	global speed
	global SnakeIsDead
	global SnakeDirection
        global DL
	remove = True

	last = snake[-1]
	first = snake[0]

	next = list(last)

	if SnakeDirection == (1,0):
		if last[0] + 1 == 8:
			next[0] = 0
		else:
			next[0] = last[0] + 1

	elif SnakeDirection == (-1,0):
		if last[0] - 1 == -1:
			next[0] = 7
		else:
			next[0] = last[0] - 1

	elif SnakeDirection == (0,1):
		if last[1] + 1 == 8:
			next[1] = 0
		else:
			next[1] = last[1] + 1

	elif SnakeDirection == (0,-1):
		if last[1] - 1 == -1:
			next[1] = 7
		else:
			next[1] = last[1] - 1

	if next in snake:
		GameOver()
	else:
		snake.append(next)

	sense.set_pixel(next[0], next[1], white)
	sense.set_pixel(first[0], first[1], blank)

	if len(foodToEat) < 3 and randint(1,5) > 4:
		Create_Point()

	if next in foodToEat and DL== "Hard":
		foodToEat.remove(next)
		sense.set_pixel(first[0], first[1], white)
		scorePoint = scorePoint + 3
		remove = False
	elif next in foodToEat and DL == "Moderate":
		foodToEat.remove(next)
		scorePoint = scorePoint + 2
		if scorePoint % 3 ==0:
			remove = False
			speed= speed * 0.8
	elif next in foodToEat and DL == "Easy":
		foodToEat.remove(next)
		scorePoint= scorePoint + 1
		if scorePoint % 5 ==0:
			remove = False
			speed=speed*0.8

 	if remove == True:
		snake.remove(first)

def difficultylevel(p):

        global speed;

	if p == "Hard":
		speed =  0.15
        elif p == "Moderate":
		speed = 0.35
	elif  p == "Easy":
		speed= 0.5

def Snake_Movement(x,y,z):

	global SnakeDirection, up, down, right, left;
	if y>0 and SnakeDirection != up:
		SnakeDirection = down
	elif y<0 and SnakeDirection != down:
		SnakeDirection = up
	elif x<0 and SnakeDirection != right:
		SnakeDirection = left
	elif x>0 and SnakeDirection != left:
		SnakeDirection = right

def Joystick_moved(event):
	global direction
	direction = event.direction

def Create_Point():
	new = snake[0]
	while new in snake:
		x = randint(0,7)
		y = randint(0,7)
		new = [x,y]
	sense.set_pixel(new[0],new[1], red)
	foodToEat.append(new)

def GameOver():
	SnakeIsDead = True
	i = 0
	while i<4:
		if(i%2) == 0:
			sense.clear(255,0,0)
			sleep(1)
		else:
			sense.clear()
			sleep(1)
		i = i+1
	sleep(2)

	sense.show_message("Game Over", text_colour=[255,0,0])
	msg ="Score: {}".format(scorePoint)
	sense.show_message(msg, text_colour=[255,0,0])
	sense.clear()
	exit(0)


sense.show_message("Let The Game Begin :)", text_colour=[255,0,0])
sense.show_message("Select difficulty level by moving joystick Right = Hard, Left= Moderate, Down= Easy")
time.sleep(2)
sense.stick.direction_any= Joystick_moved

if direction == "right":
	sense.show_message("Hard selected")
	DL= "Hard"
elif direction ==  "left":
	sense.show_message("Moderate selected")
	DL= "Moderate"
elif direction == "down":
	sense.show_message("Easy selected")
	DL= "Easy"

difficultylevel(DL)

Draw_Snake()
Create_Point()

sense.stick.direction_any = Joystick_moved
while SnakeIsDead != True:
	Move()
	sleep(speed)

	acceleration = sense.get_accelerometer_raw()
	x= acceleration['x']
	y= acceleration['y']
	z= acceleration['z']

	x=round(x,0)
	y=round(y,0)
	z=round(z,0)
	Snake_Movement(x,y,z)

sense.clear()
