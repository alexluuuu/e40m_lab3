"""main.py 

Controller + interface for playing snake
"""
import curses
import serial
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from curses import wrapper

from random import randint

import tkinter as tk
import time 
import os 
import sys


def update_board_state(snake, food, ser): 
	"""updates board state using serial output
	
	Args:
		snake (TYPE): Description
		food (TYPE): Description
	"""
	if ser is None: 
		return 

	test_file = "out.txt"
	grid = [['0' for i in range(10)] for j in range(10)]

	for part in snake: 
		grid[part[0]][part[1]] = '1'

	grid[food[0]][food[0]] = '1'

	grid_str = "".join(["".join(row[1:-1]) for row in grid[1:-1]]) + "\n"
	ser.write(grid_str.encode())


def display_score_state(food, ser):  
	pass

def curses_main(ser): 
	"""runs the snake program

	"""
	curses.initscr()
	win = curses.newwin(10, 10, 0, 0)
	win.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	win.border(0)
	win.nodelay(1)

	key = KEY_RIGHT                                                    # Initializing values
	score = 0

	snake = [[3,5], [3,4]]                                     # Initial snake co-ordinates
	food = [5,5]                                                     # First food co-ordinates

	win.addch(food[0], food[1], '*')                                   # Prints the food

	update_board_state(snake, food, ser)

	while key != 27:                                                   # While Esc key is not pressed
# 		win.border(0)
		win.timeout(300 - (len(snake)//5 + len(snake)//10)%120)          # Increases the speed of Snake as its length increases
		
		prevKey = key                                                  # Previous key pressed
		event = win.getch()
		key = key if event == -1 else event 


		if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
			key = -1                                                   # one (Pause/Resume)
			while key != ord(' '):
				key = win.getch()
			key = prevKey
			continue

		if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
			key = prevKey

		# Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
		snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

		# If snake crosses the boundaries, make it enter from the other side
		# note that snake[0] gives [x,y] list of snake head
		# snake[0][0] is x coord
		# snake[0][1] is y coord

		if snake[0][0] == 0:			# check if snake is at top row; if so, move head to bottom row 
			snake[0][0] = 8
		if snake[0][0] == 9: 
			snake[0][0] = 1
		if snake[0][1] == 0: 			# check if snake is at right column; if so, move head to left column
			snake[0][1] = 8
		if snake[0][1] == 9: 
			snake[0][1] = 1

		# if snake[0][0] == 0 or snake[0][0] == 8 or snake[0][1] == 0 or snake[0][1] == 59: 
		# 	break

		# If snake runs over itself
		if snake[0] in snake[1:]: 
			break

		if snake[0] == food:                                            # When snake eats the food
			food = []
			score += 1
			while food == []:
				food = [randint(2, 7), randint(2, 7)]                 # Calculating next food's coordinates
				if food in snake: 
					food = []
			win.addch(food[0], food[1], '*')
		else:    
			last = snake.pop()                                          # [1] If it does not eat the food, length decreases
			win.addch(last[0], last[1], ' ')

		win.addch(snake[0][0], snake[0][1], '#')
		update_board_state(snake, food, ser)
	


	curses.nocbreak()
	win.keypad(False)
	curses.echo()

	curses.endwin()

	print("\nScore - " + str(score))


def key(event): 

	if event.keysym == 'Escape':
		root.destroy()
	if event.char == event.keysym:
		# normal number and letter characters
		print( 'Normal Key %r' % event.char )
	elif len(event.char) == 1:
		# charcters like []/.,><#$ also Return and ctrl/key
		print( 'Punctuation Key %r (%r)' % (event.keysym, event.char) )	
	else:
		# f1 to f12, shift keys, caps lock, Home, End, Delete ...
		print( 'Special Key %r' % event.keysym )


def tk_main(): 
	root = tk.Tk()
	print( "Press a key (Escape key to exit):" )
	root.bind_all('<Key>', key)
	# don't show the tk window
	# root.withdraw()
	root.mainloop()

if __name__ == "__main__": 
	ser = serial.Serial(
		port='\\\\.\\COM6',
		baudrate=115200,
		parity=serial.PARITY_ODD,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)

	# ser = None
	# update_board_state([[3,5], [3,4], [3,3]] , [5,5])
	# curses_main()
	wrapper(curses_main(ser))
	# tk_main()