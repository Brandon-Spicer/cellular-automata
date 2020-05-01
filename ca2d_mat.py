"""2D cellular automaton simulator/visualizer
"""

import time
import numpy as np
import pygame as pg
import matplotlib.pyplot as plt
from itertools import product

class CellularAutomaton:
	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns
		self.grid = np.zeros((self.rows, self.columns))
		self.next_grid = self.grid.copy()
		self.hood = {(0,1), (1,1), (1,0), (0,-1), (-1,-1), (-1,0), (-1,1), (1,-1)}
		self.live_rule= {2, 3}  		# if cell is alive, what values of live neighbors will make it live next
		self.dead_rule = {3} 		# if cell is dead, what values of live neighbors will make it live next
		self.history = []
		
	def describe(self):
		print(f'Rows: {self.rows}')
		print(f'Columns: {self.columns}')
		print(f'Live cells: {self.grid.sum()}')
		print(f'Live next: {self.next_grid.sum()}')
		print(f'Hood size: {len(self.hood)}')
		print(f'Live rule: {self.live_rule}')
		print(f'Dead rule: {self.dead_rule}')
		print(f'Saved: {len(self.history)}')

	def randomize(self, ratio=0.5):
		rng = np.random.default_rng()
		self.grid = rng.random([self.rows, self.columns]) > ratio

	def kill_all(self):
		self.grid = np.zeros([self.rows, self.columns])

	def input_hood(self):
		# get coordinates for anchor node:
		x_anchor, y_anchor = (self.rows // 2, self.columns // 2)
		x_pointer, y_pointer = (self.rows // 2, self.columns // 2) 
		keymap = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

		size = 5
		black, red, green, blue = (0,0,0), (255,0,0), (0,255,0), (0,0,255)
		input_set = set([(x + x_anchor, y + y_anchor) for x, y in self.hood])

		pg.init()
		screen = pg.display.set_mode((size * self.columns, size * self.rows))
		pg.display.set_caption("Input neighborhood")

		# game loop
		running = True
		while running:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False

				# Use w/a/s/d to move, j to make, k to kill
				if event.type == pg.KEYDOWN:
					if event.unicode in keymap.keys():
						x_move, y_move = keymap[event.unicode]
						x_pointer += x_move
						y_pointer += y_move
					if event.unicode == 'j':
						input_set.add((x_pointer, y_pointer))
					if event.unicode == 'k':
						input_set = input_set - {(x_pointer, y_pointer)}

			screen.fill(black)
			# display input_set
			for x, y in input_set:
				pg.draw.rect(screen, red, (x * size, y * size, size, size))
			# draw anchor node
			pg.draw.rect(screen, green, (x_anchor * size, y_anchor * size, size, size))
			# draw pointer node outline
			pg.draw.rect(screen, green, (x_pointer * size, y_pointer * size, size, size), width=1)
			pg.display.update()
		pg.quit()

		# for every point in inputSet, we need to subtract off our anchor point and add that to neighborhood
		for x, y in input_set:
			self.hood.add((x - x_anchor, y - y_anchor))

	def evolve(self, limit=-1, save=True, viz=True, size=5, live_color=(255,0,0), dead_color=(0,0,0)):
		history = []
		steps = 0
		pg.init()
		screen = pg.display.set_mode((size * self.rows, size * self.columns))
		pg.display.set_caption('Cellular Automaton 2D (Matrix version)')
		
		# pygame loop
		running = True
		while running:
			# check for quit
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
			# store history
			if save:
				history.append(self.grid)
			# visualize with pygame
			if viz:
				self.display(screen, size=size)
			# track steps
			steps += 1
			if steps > limit > 0:
				running = False

			# update the grid
			self.calc_next()

		if save:
			self.history.append(np.array(history))
			return np.array(history)

	# vectorized function that implements a single time step of the CA
	def calc_next(self):
		# ngrid contains the number of live neighbors for each cell
		ngrid = 0
		for n, m in self.hood:
			ngrid += np.roll(self.grid, (n, m), axis=(0,1))

		# calculate next_grid from grid and ngrid
		live_mask = np.isin(ngrid, list(self.live_rule))
		dead_mask = np.isin(ngrid, list(self.dead_rule))
		self.next_grid = np.where(self.grid, live_mask, dead_mask)

		self.grid = self.next_grid.copy()

	def animate(self, game = None, tick = 0.1):
		if game == None:
			game = self.history[-1]
		size = 5
		black, red, green, blue = (0,0,0), (255,0,0), (0,255,0), (0,0,255)
		pg.init()
		screen = pg.display.set_mode((size * self.rows, size * self.columns))
		index = 0

		# pygame loop
		running = True
		paused = False
		while running:
			pg.display.set_caption(f'Cellular Automata 2D (Matrix version) | index = {index}')
			# check events
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				if event.type == pg.KEYDOWN:
					# Spacebar to puase/play
					if event.key == pg.K_SPACE:
						paused = not paused
					# If paused, use k/j to step forward/back
					if paused and event.key == pg.K_k:
						index += 1
						self.display_index(screen, game, index, black, red)
					if paused and event.key == pg.K_j:
						index -= 1
						self.display_index(screen, game, index, black, red)
			if not paused:
				# display the grid for given index
				self.display_index(screen, game, index, black, red)
				# time delay
				time.sleep(tick)

				# check if index out of range
				index += 1
				if index >= len(game):
					running = False

	# Display game at given index
	def display_index(self, screen, game, index, dead_color, live_color):
		size = 5
		screen.fill(dead_color)
		for i, j in product(range(game[index].shape[0]), range(game[index].shape[1])):
			if game[index][i][j]:
				pg.draw.rect(screen, live_color, (i*size, j*size, size, size))
		pg.display.update()
		
	# displays the current grid to a given pygame screen
	def display(self, screen, size=5):
		screen.fill((0,0,0))
		for i, j in product(range(self.rows), range(self.columns)):
			if self.grid[i][j]:
				pg.draw.rect(screen, (255,0,0), (i*size, j*size, size, size))
		pg.display.update()



if __name__ == '__main__':
	game = CellularAutomaton(100, 100)
	game.randomize()
	game.evolve(size = 5) 
