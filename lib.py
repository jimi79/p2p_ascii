import random
import curses

value_good = ['mars', 'venus', 'mercure', 'earth', 'uranus', 'jupiter', 'neptune', 'saturn']
value_bad = ['thieves', 'steal', 'pirates', 'hackers']

min_=4
max_=10

class Block:
	def __init__(self):
		self.value = 3

	def init(self): 
		#self.value = self.get_random_value(bad)
		#self.value = ''.join([random.choice('0123456789abcdef') for i in range(0, 10)])
		self.value = random.randrange(min_, max_)
		self.block_number = -1

	def copy(self):
		b = Block()
		b.value = self.value
		b.block_number = self.block_number
		return b

class Chain:
	def __init__(self):
		self.blocks = []

	def add(self):
		#self.blocks = self.blocks[-4:]
		block = Block()
		block.init()
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

	def draw(self):
		self.stdscr.addstr(self.line*6+0, self.col*14, '┌──────────┐')
		self.stdscr.addstr(self.line*6+1, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+2, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+3, self.col*14, '│          │')
		self.stdscr.addstr(self.line*6+4, self.col*14, '└──────────┘')
		for l in self.linked_to:
			if (l.line == self.line + 1) and (l.col == self.col):
				self.stdscr.addstr(self.line*6+5, self.col*14+6, '│')
			if (l.line == self.line) and (l.col == self.col + 1):
				self.stdscr.addstr(self.line*6+2, self.col*14+12, '──') 

	def print_content_3(self):
		if self.chain.length() > 0:
			for i in range(1, 4): 
				if self.chain.length() > i:
					self.stdscr.addstr(self.line*6+i, self.col*14+1, '          ', curses.color_pair(self.chain.blocks[-i].value))

	def print_content(self):
		self.print_content_3()

	def copy_from_neighbour(self, neighbour): 
		for block in neighbour.chain.blocks[self.new_chain.length():]:
			self.new_chain.blocks.append(block.copy())

	def copy_from_neighbour_if_ok(self, neighbour):
		if self.new_chain.length() == 0:
			self.copy_from_neighbour(neighbour)
		else:
			self.copy_from_neighbour(neighbour)

	def copy_from_neighbour(self, neighbour):
		self.new_chain = neighbour.chain.copy()
		a = sum([block.value for block in self.chain.blocks])
		b = sum([block.value for block in self.new_chain.blocks[0:self.chain.length()]])
		if a != b:
			self.wrong = self.wrong + 1

	def write_line(self, i, s):
		self.stdscr.addstr(self.line*6+1+i, self.col*14+1, s)

	def get_content_from_neighours(self):
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

	def time_shift(self):
		self.chain = self.new_chain

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

	def propagate_content(self):
		for comp in self.list:
			comp.get_content_from_neighours()

	def time_shift(self): 
		for comp in self.list:
			comp.time_shift()

	def add_random(self):
		random.choice(self.list).chain.add()

	def max_length(self):
		return max([comp.chain.length() for comp in self.list])

class Links:
	def __init__(self, computers):
		self.links = []
		for i in range(0, computers.lines):	
			for j in range(0, computers.cols):	
				comp = computers.list[i * computers.cols + j]
				if j < computers.cols - 1:
					comp_to_the_right = computers.list[i * computers.cols + j + 1]
					self.links.append((comp, comp_to_the_right))
				if i < computers.lines - 1:
					comp_underneath = computers.list[(i + 1) * computers.cols + j] 
					self.links.append((comp, comp_underneath))

	def remove_some(self, count = 40):
		for i in range(0, count):
			if len(self.links) > 0:
				self.links.pop(random.randrange(0, len(self.links)))


	def apply(self, computers):
		for link in self.links:
			link[0].linked_to.append(link[1])
			link[1].linked_to.append(link[0])
