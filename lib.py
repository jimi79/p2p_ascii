import random
import curses
import shutil
import sys

value_good = ['mars', 'venus', 'mercure', 'earth', 'uranus', 'jupiter', 'neptune', 'saturn']
value_bad = ['thieves', 'steal', 'pirates', 'hackers']

def debug(s):
	open("debug.log", "a").write("%s\n" % s)


class Block:
	def copy(self):
		b = Block()
		b.value = self.value
		b.color = self.color
		b.block_number = self.block_number
		return b

class Chain:
	def __init__(self):
		self.blocks = []

	def add(self, value, color):
		#self.blocks = self.blocks[-4:]
		block = Block()
		block.value = value
		block.color = color
		block.block_number = len(self.blocks)
		self.blocks.append(block) 

	def length(self):
		return len(self.blocks)

	def copy(self):
		c = Chain()
		for block in self.blocks:
			b = block.copy()
			c.blocks.append(b)
		return c

class Computer:
	def __init__(self, stdscr, line, col):
		self.chain = Chain()
		self.stdscr = stdscr
		self.line = line
		self.col = col
		self.linked_to = []
		self.wrong = 0
		self.new_chain = None

	def draw(self):
		self.stdscr.addstr(self.line*6+0, self.col*14, '┌──────────┐')
		self.stdscr.addstr(self.line*6+1, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+2, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+3, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+4, self.col*14, '└──────────┘')
	
	def draw_links(self):
		self.stdscr.addstr(self.line*6+5, self.col*14+6, ' ')
		self.stdscr.addstr(self.line*6+2, self.col*14+12, '  ') 
		for l in self.linked_to:
			if (l.line == self.line + 1) and (l.col == self.col):
				self.stdscr.addstr(self.line*6+5, self.col*14+6, '│')
			if (l.line == self.line) and (l.col == self.col + 1):
				self.stdscr.addstr(self.line*6+2, self.col*14+12, '──') 

	def print_content_3(self):
		if self.chain.length() == 0:
			return 
		color = self.chain.blocks[-1].color
		self.stdscr.addstr(self.line*6+1, self.col*14+1, '   %03d    ' % self.chain.length(), curses.color_pair(color))
		if self.chain.length() == 1:
			return
		color = self.chain.blocks[-2].color

		self.stdscr.addstr(self.line*6+2, self.col*14+1, '          ', curses.color_pair(color))
		if self.chain.length() == 2:
			return 
		color = self.chain.blocks[-3].color
		s = ''.join([b.value for b in self.chain.blocks[-10:]])
		s = s.ljust(10, ' ')
		self.stdscr.addstr(self.line*6+3, self.col*14+1, s, curses.color_pair(color))

	def print_content(self):
		self.print_content_3()

	def copy_from_neighbour(self, neighbour): 
		self.new_chain = []
		for block in neighbour.chain.blocks[self.new_chain.length():]:
			self.new_chain.blocks.append(block.copy())

	def copy_from_neighbour_if_ok(self, neighbour):
		if self.new_chain.length() == 0:
			self.copy_from_neighbour(neighbour)
		else:
			self.copy_from_neighbour(neighbour)

	def copy_from_neighbour(self, neighbour):
		self.new_chain = neighbour.chain.copy()
		# find a new way to find out if it's wrong, but i don't care for now
		#a = sum([block.value for block in self.chain.blocks])
		#b = sum([block.value for block in self.new_chain.blocks[0:self.chain.length()]])
		#if a != b:
		#	self.wrong = self.wrong + 1

	def write_line(self, i, s):
		self.stdscr.addstr(self.line*6+1+i, self.col*14+1, s)

	def get_content_from_neighours(self):
		if self.new_chain == None:
			self.new_chain = self.chain.copy()
		i = 0
		best = None
		best_length = self.new_chain.length()
		for comp in self.linked_to:
			#self.write_line(i, "%d %d" % (comp.chain.length(), best_length))
			if comp.chain.length() > best_length:
				best = comp
				best_length = comp.chain.length()
			i = i + 1 
		if best != None:
			self.copy_from_neighbour(best)
			return True
		return False

	def time_shift(self):
		self.chain = self.new_chain
		self.new_chaine = None

class Computers:
	def __init__(self, stdscr, colors, values, cols = None, lines = None):
		self.cols = None
		self.lines = None
		if (cols == None)	or (lines == None):
			term_cols, term_lines = shutil.get_terminal_size(fallback=(80,24))
			if (cols == None):
				self.cols = term_cols // 14
			if (lines == None):
				self.lines = term_lines // 6

		if self.cols == None:
			self.cols = cols
		if self.lines == None:
			self.lines = lines
		self.count = self.cols * self.lines
		self.list = []
		self.colors = colors
		self.values = values
		self.idx_col = 0
		random.shuffle(self.colors)
		for i in range(0, self.lines):
			for j in range(0, self.cols):
				self.list.append(Computer(stdscr, i, j))
	
	def draw(self):
		for i in range(self.count):
			self.list[i].draw()

	def draw_links(self):
		for i in range(self.count):
			self.list[i].draw_links()

	def print_content(self):
		for i in range(self.count):
			self.list[i].print_content()

	def propagate_content(self):
		updated = True
		while updated:
			updated = False
			for comp in self.list:
				if comp.get_content_from_neighours():
					updated = True
		for comp in self.list:
			comp.time_shift()

	def add_random(self):
		comp = random.choice(self.list)
		comp.chain.add(self.values[self.idx_col], self.colors[self.idx_col])
		self.idx_col = (self.idx_col + 1) % len(self.colors)

	def max_length(self):
		return max([comp.chain.length() for comp in self.list])

class Link:
	def __init__(self, src, dst, enabled = True):
		self.src = src
		self.dst = dst
		self.enabled = True

class Links:
	def __init__(self, computers):
		self.links = []
		self.computers = computers

	def link_all(self):
		for i in range(0, self.computers.lines):	
			for j in range(0, self.computers.cols):	
				comp = self.computers.list[i * self.computers.cols + j]
				if j < self.computers.cols - 1:
					comp_to_the_right = self.computers.list[i * self.computers.cols + j + 1]
					self.links.append(Link(comp, comp_to_the_right))
				if i < self.computers.lines - 1:
					comp_underneath = self.computers.list[(i + 1) * self.computers.cols + j] 
					self.links.append(Link(comp, comp_underneath))

	def switch_some(self, count = 40):
		for i in range(0, count):
			link = random.choice(self.links)
			link.enabled = not link.enabled
			link.src.draw_links()
			
	def disable_some(self, count = None, ratio = None):
		if count == None:
			if ratio == None:
				ratio = 0.5
			count = int(len(self.links) * ratio)
		for i in range(0, count):
			link = random.choice(self.links)
			link.enabled = False

	def apply(self):
		for comp in self.computers.list:
			comp.linked_to = []
		for link in self.links:
			if link.enabled:
				link.src.linked_to.append(link.dst)
				link.dst.linked_to.append(link.src)
