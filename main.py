#!/usr/bin/python3

import lib
import curses
import random
import time


#https://docs.python.org/3/howto/curses.html

def main(stdscr):
	stdscr.clear() 
	curses.curs_set(False)
	computers = lib.Computers(stdscr)
	curses.init_pair(1, curses.COLOR_RED, 0)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)


	curses.init_pair(4, 0, curses.COLOR_RED)
	curses.init_pair(5, 0, curses.COLOR_GREEN)
	curses.init_pair(6, 0, curses.COLOR_YELLOW)
	curses.init_pair(7, 0, curses.COLOR_BLUE)
	curses.init_pair(8, 0, curses.COLOR_MAGENTA)
	curses.init_pair(9, 0, curses.COLOR_CYAN)
	curses.init_pair(10, 0, curses.COLOR_WHITE)

	curses.halfdelay(1)

	#test

	l = lib.Links(computers)
	l.remove_some(60)
	l.apply(computers)
	computers.draw() 
	computers.print_content() 

	a = ''
	c = 1
	while (a != 'q') or (computers.max_length > 100): 
		if random.randrange(0, 10) == 0:
			computers.add_random()
		#if (a == ' '):
		#	computers.add_random()
		#	a = '' 
		#c = c + 1 
		computers.propagate_content()
		computers.time_shift()
		computers.print_content() 
		time.sleep(0.1)
		stdscr.refresh()
		try:
			a = stdscr.getkey()
		except:
			pass



curses.wrapper(main)
