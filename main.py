"""main.py 

Controller + interface for playing snake
"""

# external dependencies
import curses
import serial
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from curses import wrapper
from random import randint
import time 
import os 
import sys

# internal dependencies
from render_text import render_text
from board_letters import get_letter


def update_board_state(snake, food, ser): 
	"""updates board state using serial output
	
	Args:
		snake (List(List)): list of lists representing (x,y) snake pos coordinates
		food (List): (x,y) position representing food location
	"""
	# for debugging purposes, return if we can't write to Serial monitor
	if ser is None: 
		return 

	# initialize empty grid 
	grid = [['0' for i in range(10)] for j in range(10)]

	# highlight grid entries with snake 
	for part in snake: 
		grid[part[0]][part[1]] = '1'

	# add food to grid
	grid[food[0]][food[0]] = '1'

	# reshape grid into 1D, convert to string, add linebreak
	grid_str = "".join(["".join(row[1:-1]) for row in grid[1:-1]]) + "\n"

	# write Serial output
	ser.write(grid_str.encode())

	return


def display_score_state(win, ser, score):  
	"""display_score_state
	
	Args:
	    win (curses window): window for curses, used for debugging dispaly simulation
	    ser (serial monitor object): used for communicating with the board through serial output
	    score (int): score obtained through playing snake

 
	Function used to display the score state after you've died in snake :) 
	Uses function in board_letters.py to retrieve the grid state for each letter in the target message

	"""
	# produce message, display
	message = "Your score: " + str(score)
	render_text(message, ser)

	# Display score only a couple of extra times for extra spice
	render_text(str(score), ser)
	render_text(str(score), ser)

	return 


def curses_main(ser): 
	"""runs the snake program

	"""

	# initialize curses display
	curses.initscr()
	win = curses.newwin(10, 10, 0, 0)
	win.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	win.border(0)
	win.nodelay(1)

	key = KEY_RIGHT                                                  
	score = 0

	snake = [[3,5], [3,4]]                                     
	food = [5,5]                                                     

	win.addch(food[0], food[1], '*')                                   

	update_board_state(snake, food, ser)

	# While Esc key is not pressed
	while key != 27:                                                   
		win.timeout(300 - (len(snake)//5 + len(snake)//10)%120)          
		
		prevKey = key                                                  
		event = win.getch()
		key = key if event == -1 else event 


		# If SPACE BAR is pressed, wait for another
		if key == ord(' '):                                            
			key = -1                                                   
			while key != ord(' '):
				key = win.getch()
			key = prevKey
			continue

		# If an invalid key is pressed
		if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     
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

		# If snake runs over itself
		if snake[0] in snake[1:]: 
			break

		
		# at each iteration, check if we've gotten the food 
		# if we have gotten the food: 			
		# 	produce new food, don't change snake
		# otherwise:							
		# 	leave food alone, take off the end of the snake to simulate crawling motion
		if snake[0] == food:                                            
			food = []
			score += 1
			while food == []:
				# next food position
				food = [randint(2, 7), randint(2, 7)]                 
				if food in snake: 
					food = []
			win.addch(food[0], food[1], '*')
		else:    
			last = snake.pop()                                          
			win.addch(last[0], last[1], ' ')

		# update the head of the snake
		win.addch(snake[0][0], snake[0][1], '#')

		# write to the board
		update_board_state(snake, food, ser)
	

	display_score_state(win, ser, score)

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


if __name__ == "__main__": 

	# initialize Serial monitor
	ser = serial.Serial(
		port='\\\\.\\COM6',
		baudrate=115200,
		parity=serial.PARITY_ODD,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)

	# for debugging: 
	# ser = None
	# update_board_state([[3,5], [3,4], [3,3]] , [5,5])

	# welcome message
	render_text("Welcome To Snake!", ser)

	# game main
	wrapper(curses_main(ser))

	# exit message
	render_text("Come back again!", ser)
