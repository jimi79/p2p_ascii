import random
import curses

value_good = ['mars', 'venus', 'mercure', 'earth', 'uranus', 'jupiter', 'neptune', 'saturn']
value_bad = ['thieves', 'steal', 'pirates', 'hackers']



class Block:
	def get_random_value(self, bad):
		if not bad:
			return random.choice(value_good)
		else:
			return random.choice(value_bad)

	def __init__(self, bad): 
		self.value = self.get_random_value(bad)
		hash_ = sum([ord(s) for s in self.value]) % 10
		self.block_number = -1
		self.bad = bad

	def copy():
		b = Block()
		b.value = self.value
		b.hash = self.hash
		b.block_number = self.block_number
		b.bad = self.bad
		return b

class Chain:
	def __init__(self):
		self.blocks = []

	def add(self, bad):
		self.blocks = self.blocks[-4:]
		block = Block(bad)
		block.block_number = len(self.blocks)
		self.blocks.append(block) 


class Computer:
	def __init__(self, stdscr, line, col):
		self.chain = Chain()
		self.stdscr = stdscr
		self.line = line
		self.col = col

	def draw(self):
		self.stdscr.addstr(self.line*6+0, self.col*14, '┌──────────┐')
		self.stdscr.addstr(self.line*6+1, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+2, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+3, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+4, self.col*14, '└──────────┘')

	def print_content(self):
		i = 0
		for block in self.chain.blocks[-5:]:
			if block.bad:
				self.stdscr.addstr(self.line*6+1, self.col*14+1+i, block.value[0:10], curses.color_pair(1))
			else: 
				self.stdscr.addstr(self.line*6+1, self.col*14+1+i, block.value[0:10])
			i = i + 1

class Computers:
	def __init__(self, stdscr):
		self.cols = 12
		self.lines = 8 
		self.count = self.cols * self.lines
		self.list = []
		for i in range(0, self.lines):
			for j in range(0, self.cols):
				self.list.append(Computer(stdscr, i, j))
	
	def draw(self):
		for i in range(self.count):
			self.list[i].draw()

	def print_content(self):
		for i in range(self.count):
			self.list[i].print_content()
	
class Links:
# will apply some random links to all computers
# will apply first all links
# then remove some
# then apply to each computers
# each comp will draw its own links
# dotted line for links
