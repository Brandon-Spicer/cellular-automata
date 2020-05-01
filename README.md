# cellular-automata
A project to build flexible and functional tools to calculate, customize, analyze, and visualize cellular automata.

`ca2d_mat` is a simple implementation of a general 2D cellular automaton in python.
It uses numpy for calculation and pygame for visualization.

Documentation coming soon. Here are a few usage examples:

### Run Conway's Game of Life

```python
from ca2d_mat import CellularAutomaton 
ca = CellularAutomaton(100, 100)
ca.randomize()
ca.evolve()
```
Close the pygame window to quit.

### Visualize a historical game

Unless `save=False` is passed to `ca.evolve()`, games are stored in `ca.history`.
You can specify which historical game to use by index (`ca.history[5]`).
By default, the most recent saved game is used.

```python
from ca2d_mat import CellularAutomaton 
ca = CellularAutomaton(100, 100)
ca.randomize()
ca.evolve(limit=100)

ca.animate()
```

Use `SPACE` to pause/play, and use `k/j` to step forward/back when paused.


### Inputting a custom neighborhood and rules

The neighborhood `ca.hood` is a set of tuples describing the locations of neighbors relative to a cell at (0,0).
The rule is encoded as two sets, `ca.live_rule` and `ca.dead_rule`.
<br />
`ca.live_rule` contains integers that represent the number of live neighbors that would cause a live cell to continue to live.
<br />
`ca.dead_rule` contains integers that represent the number of live neighbors that would cause a dead cell to come to life.
<br />
If the number of live neighbors is not in the rule, then the cell dies.
So, for example, Conway's Game of Life is defined by:
<br />

`ca.hood = {(0,1), (1,1), (1,0), (0,-1), (-1,-1), (-1,0), (-1,1), (1,-1)}`
<br />
`ca.live_rule = {2, 3}`
<br />
`ca.dead_rule = {3}`

These are the default values.

You can use `input_hood` to visually input a custom neighborhood.

```python
from ca2d_mat import CellularAutomaton
ca = CellularAutomaton(100, 100)
ca.input_hood()
```
Use `w/a/s/d` to move the cursor, and `j/k` to add/remove neighbors.
Close the pygame window when finished, and the neighborhood will automatically update.

```python
ca.live_rule = {1, 2, 3, 4, 5}
ca.dead_rule = {3, 4, 5}
ca.randomize(ratio=0.2)
ca.evolve()
```


