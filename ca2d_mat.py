"""2D cellular automaton simulator/visualizer
"""

import time
import os
import numpy as np
import pandas as pd
import pygame as pg
from itertools import product
try:
    import cPickle as pickle
except:
    import pickle

# TODO: Make 1D CA.

class CA:
    # Load files
    if os.path.exists('history.pickle'):
        with open('history.pickle', 'rb') as pickle_in:
            history = pickle.load(pickle_in)
    if os.path.exists('rules.pickle'):
        with open('rules.pickle', 'rb') as pickle_in:
            rules_table = pickle.load(pickle_in)

    # Pygame variables
    size = 5
    Black = np.array((0,0,0))
    White = np.array((255,255,255))
    Red = np.array((255,0,0))
    Lime = np.array((0,255,0))
    Blue = np.array((0,0,255))
    Yellow = np.array((255,255,0))
    Cyan = np.array((0,255,255))
    Magenta	= np.array((255,0,255))
    Silver = np.array((192,192,192))
    Gray = np.array((128,128,128))
    Maroon = np.array((128,0,0))
    Olive = np.array((128,128,0))
    Green = np.array((0,128,0))
    Purple = np.array((128,0,128))
    Teal = np.array((0,128,128))
    Navy = np.array((0,0,128))


    # color lists
    default_colors = [Black, White, Red, Lime, Blue, Yellow, Cyan,\
        Magenta, Silver, Gray, Maroon, Olive, Green, Purple, Teal, Navy]
    default_colors = default_colors * 4 
    # https://www.schemecolor.com/fire-color-scheme.php
    fire_colors = [Black, (250, 192, 0), (255, 117, 0), (252, 100, 0), (215, 53, 2), (182, 34, 3), (128, 17, 0)]
    fire_colors = fire_colors * 4
    # https://www.schemecolor.com/pastel-color-tones.php
    pastel_colors = [Black, (255, 223, 211), (254, 200, 216), (210, 145, 188), (149, 125, 173), (224, 187, 228)]
    pastel_colors = pastel_colors * 4
       

    def __init__(self, rows, columns, rule='23/3/2', rule_name=None):
        self.rows = rows
        self.columns = columns
        self.grid = np.zeros((self.rows, self.columns))
        self.next_grid = self.grid.copy()
        # Default neighborhood is the Moore neighborhood
        self.hood = {(0,1), (1,1), (1,0), (0,-1), (-1,-1), (-1,0), (-1,1), (1,-1)}
        # If rule name is provided, override rule
        if rule_name is not None:
            rule = CA.rules_table[CA.rules_table.Name == rule_name].Rule.iloc[0]
        self.rule = rule
        # Get rule sets from rule string
        rule = rule.split('/')
        self.survival_rule = set(map(int, rule[0]))          
        self.birth_rule = set(map(int, rule[1]))
        self.generations = int(rule[2])
 

    def save_history(self):
        with open('history.pickle', 'wb') as pickle_out:
            pickle.dump(CA.history, pickle_out)
        
    def describe(self):
        print(f'Rows: {self.rows}')
        print(f'Columns: {self.columns}')
        print(f'Live cells: {self.grid.sum()}')
        print(f'Hood size: {len(self.hood)}')
        print(f'Neighborhood: {self.hood}')
        print(f'Live rule: {self.survival_rule}')
        print(f'Dead rule: {self.birth_rule}')
        print(f'Saved: {len(CA.history)}')

    def randomize(self, ratio=0.5, option=None, size = 3):
        rng = np.random.default_rng()
        random_grid = rng.random([self.rows, self.columns])

        if option == 'square':
            # Define coordinates
            # square is 1/5 rows by 1/5 columns and centered in the display
            x = self.rows
            y = self.columns
            x1 = (x // 2) - (x // (2 * size))
            x2 = (x // 2) + (x // (2 * size))
            y1 = (y // 2) - (y // (2 * size))
            y2 = (y // 2) + (y // (2 * size))
            
            self.grid = np.zeros([x, y])
            self.grid[x1:x2, y1:y2] = random_grid[x1:x2, y1:y2] < ratio
        else:
            self.grid = random_grid < ratio
        self.next_grid = self.grid

    def square_seed(self, size = 3, offset = (0, 0)):
        x = self.rows 
        y = self.columns
        x1 = ((x // 2) - (x // (2 * size)) + offset[0]) % x
        x2 = ((x // 2) + (x // (2 * size)) + offset[0]) % x
        y1 = ((y // 2) - (y // (2 * size)) + offset[1]) % y
        y2 = ((y // 2) + (y // (2 * size)) + offset[1]) % y

        self.grid[x1:x2, y1:y2] = 1

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
        pg.display.set_caption(f'CA2D rule: {self.rule}')
        
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
            CA.history.append(np.array(history))
            self.save_history()

    # vectorized function that implements a single time step of the CA
    def calc_next(self):
        # create only_live_grid
        live_grid = self.grid == 1
        # use that to make ngrid
        # ngrid contains the number of live neighbors for each cell
        ngrid = 0
        for n, m in self.hood:
            ngrid += np.roll(live_grid, (n, m), axis=(0,1))

        # calculate next_grid from grid and ngrid
        survival_mask = np.logical_and(self.grid == 1, np.isin(ngrid, list(self.survival_rule), invert=True))
        birth_mask = np.logical_and(self.grid == 0, np.isin(ngrid, list(self.birth_rule)))

        self.next_grid = np.where(survival_mask, (self.grid + 1) % self.generations, self.next_grid)
        self.next_grid = np.where(birth_mask, 1, self.next_grid)
        self.next_grid = np.where(self.grid >= 2, (self.grid + 1) % self.generations, self.next_grid)
                
        self.grid = self.next_grid.copy()

    def animate(self, game=None, tick=0, display_methods=['generations'], colors=None, loop=True):
        if np.all(game == None):
            game = CA.history[-1]
        if colors == None:
            colors = CA.default_colors
        size = 5
        black, white, red, green, blue = (0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255)
        pg.init()
        screen = pg.display.set_mode((size * self.rows, size * self.columns))
        index = 0
        r = 1       # reversal constant

        # pygame loop
        running = True
        paused = True 
        while running:
            # controls I want
                # skip with 0-9
                # fast forward with h/l
                # reverse with r
            pg.display.set_caption(f'CA2D Animation | r = {r != 1} | index = {index}')
            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:

                    # Spacebar to puase/play
                    if event.key == pg.K_SPACE:
                        paused = not paused
                    # If paused, use j/k to step forward/back
                    if paused and event.key == pg.K_j:
                        index += 1
                    if paused and event.key == pg.K_k:
                        index -= 1

                    if event.key == pg.K_r:
                        r = -r 
                    
                    keys = [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]
                    for k in keys:
                        if event.key == k:
                            index = (k - 48) * len(game) // 10

            if not paused:
                # time delay
                time.sleep(tick)
                # check if index out of range
                index += 1*r
                if index >= len(game):
                    index = 0

                if not loop:
                    running = False


            screen.fill(CA.Black)
            for name in display_methods:
                
                if name == 'memory':
                    self.display_memory(screen, game, index % len(game), CA.Red, 20)
                elif name == 'decay':
                    self.display_decay(screen, game, index % len(game), color_list=colors)
                elif name == 'generations':
                    self.display_generations(screen, game, index % len(game), color_list=colors) 

            pg.display.update()

    """================================ Different display functions for animate() ================================"""

    # TODO: write simple display_default function
    def display_default(self, screen, game, index, color=None):
        pass
        
    # Display game at given index
    def display_generations(self, screen, game, index, color_list):
        for i, j in product(range(game.shape[1]), range(game.shape[2])):
            gen = int(game[index][i][j])
            if game[index][i][j] != 0:
                pg.draw.rect(screen, color_list[gen], CA.size * np.array([i, j, 1, 1], np.int32))

    def display_memory(self, screen, game, index, live_color, depth):
        # define memory_grid
        memory_grid = np.zeros([self.rows, self.columns])
        # look back min(index, depth) steps in game from current index
        for d in range(min(index, depth)):
            # add up the past min(index, depth) number of grids
            memory_grid += game[index - d]
        for i, j in product(range(game.shape[1]), range(game.shape[2])):
            if game[index][i][j]:
                pg.draw.rect(screen, live_color, (i*CA.size, j*CA.size, CA.size, CA.size))
            else:
                mem_color = (memory_grid[i][j]*255)//min(index+1, depth)
                mem_color = (mem_color % 255, 0, 0)
                pg.draw.rect(screen, mem_color, (i*CA.size, j*CA.size, CA.size, CA.size))

    def display_colors(self, screen, game, index, color_list=[(0,0,0), (0,255,0), (255,0,0), (0,0,255), (255,255,255)]):
        # add up the last 3 grids
        # color based on number
        memory_grid = np.zeros([self.rows, self.columns])
        length = len(color_list)
        
        for d in range(min(index, length-1)):
            memory_grid += game[index - d]
            
        for i, j in product(range(game.shape[1]), range(game.shape[2])):
            num = int(memory_grid[i][j])
            pg.draw.rect(screen, color_list[num], (i*CA.size, j*CA.size, CA.size, CA.size))

    def display_decay(self, screen, game, index, color_list=[(0,0,0), (0,0,255), (0,255,0), (255,0,0), (255,255,255)]):
        depth = min(index, len(color_list))

        for i, j in product(range(game.shape[1]), range(game.shape[2])):
            dist = 0
            for d in range(depth-1):
                if game[index - d][i][j]:
                    break
                else:
                    dist += 1

            pg.draw.rect(screen, color_list[dist], (i*CA.size, j*CA.size, CA.size, CA.size))

                
    """ =========================================================================================="""                

    """ Display function for evolve() """        
    # displays the current grid to a given pygame screen
    def display(self, screen, size=5):
        screen.fill((0,0,0))
        for i, j in product(range(self.rows), range(self.columns)):
            if self.grid[i][j]:
                pg.draw.rect(screen, (255,0,0), (i*size, j*size, size, size))
        pg.display.update()



if __name__ == '__main__':
    game = CA(100, 100)
    game.randomize()
    game.evolve(limit=500, viz=False) 
    game.animate()
