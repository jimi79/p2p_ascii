#!/usr/bin/python3

import lib
import curses


#https://docs.python.org/3/howto/curses.html

def main(stdscr):
	stdscr.clear() 
	curses.curs_set(False)
	computers = lib.Computers(stdscr)
	curses.init_pair(1, curses.COLOR_RED, 0)
	computers.draw() 
	computers.list[5].chain.add(False)
	computers.list[6].chain.add(True)
	computers.print_content() 
	stdscr.refresh()
	stdscr.getkey()



curses.wrapper(main)
