#!/usr/bin/python3

import lib
import curses
import time


#https://docs.python.org/3/howto/curses.html

def main(stdscr):
	stdscr.clear() 
	curses.curs_set(False)
	computers = lib.Computers(stdscr)
	curses.init_pair(1, curses.COLOR_RED, 0)
	curses.halfdelay(1)

	#test

	l = lib.Links(computers)
	l.remove_some()
	l.apply(computers)
	computers.draw() 
	computers.print_content() 

	a = ''
	c = 1
	while a != 'q':


	
	#computers.list[5].chain.add(False)
	#computers.list[6].chain.add(True) 
		if c % 2 == 0:
			computers.add_random(False)


		if c % 10 == 0:
			computers.add_random(True)

		c = c + 1

		computers.propagate_content()
		computers.time_shift()
		computers.print_content() 
		time.sleep(1)
		stdscr.refresh()
		try:
			a = stdscr.getkey()
		except:
			pass



curses.wrapper(main)
