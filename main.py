#!/usr/bin/python3

import lib
import curses
import random
import time
import argparse

#https://docs.python.org/3/howto/curses.html



global debug_var

def run(stdscr):
	computers = lib.Computers(stdscr, [4, 5, 6, 7, 8, 9, 10], ['1', '2', '3', '4', '5', '6', '7']) 
	curses.halfdelay(1) 
	l = lib.Links(computers)
	l.link_all()
	l.disable_some()
	l.apply()
	computers.draw() 
	computers.draw_links()
	computers.print_content() 

	a = ''
	c = 0

	while (a != 'q') and (computers.max_length() < 200): 
# add a value
		if c % 5 == 0:
			computers.add_random()

# change links
		if c % 100 == 0:
			l = lib.Links(computers)
			l.link_all()
			l.disable_some()
			l.apply()
			computers.draw_links()

		c = (c + 1) % 100

		#if (a == ' '):
		#	computers.add_random()
		#	a = '' 
		#c = c + 1 
		computers.propagate_content()
		computers.print_content() 
		time.sleep(0.01)
		stdscr.refresh()
		try:
			a = stdscr.getkey()
		except:
			pass

#	global debug_var
#	debug_var = {}
#	debug_var['l'] = l



def run_test(stdscr):
	computers = lib.Computers(stdscr, [4, 5, 6, 7, 8, 9, 10], cols = 2, lines = 2) 
	l = lib.Links(computers)
	l.links.append(lib.Link(computers.list[0], computers.list[2]))
	l.links.append(lib.Link(computers.list[1], computers.list[3]))
	l.links.append(lib.Link(computers.list[2], computers.list[3]))
	l.apply()
	computers.draw() 
	computers.draw_links()
	computers.list[0].chain.add(5)
	for i in range(0,3):
		computers.propagate_content()
		computers.print_content()
		a = stdscr.getkey()

def main(stdscr, test):
	stdscr.clear() 
	curses.curs_set(False)
	curses.init_pair(1, curses.COLOR_RED, 0)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) 
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(5, 0, curses.COLOR_GREEN)
	curses.init_pair(6, 0, curses.COLOR_YELLOW)
	curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
	curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
	curses.init_pair(9, 0, curses.COLOR_CYAN)
	curses.init_pair(10, 0, curses.COLOR_WHITE) 
	if test:
		run_test(stdscr)
	else:
		run(stdscr)

def parse_arguments():
	parser = argparse.ArgumentParser(description='display some stuff')
	parser.add_argument('--test', dest='test', action='store_const', const=True, default=None)
	return parser.parse_args()

args = parse_arguments()
curses.wrapper(main, args.test)
