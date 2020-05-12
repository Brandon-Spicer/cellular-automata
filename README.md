# cellular-automata
A python module for creating and visualizing multi-generational 2-dimensional cellular automata (CA).

### Quickstart: Run Conway's Game of Life

```python
from ca2d_mat import CA 
ca = CA(100, 100)
ca.randomize()
ca.evolve()
```
Close the pygame window to quit.

### Visualize a historical game

Unless `save=False` is passed to `ca.evolve()`, games are stored in `CA.history`.
You can specify which historical game to use by index (`ca.history[5]`).
By default, the most recent saved game is used.

```python
from ca2d_mat import CA 
ca = CA(100, 100)
ca.randomize()
ca.evolve(tick=0.1)

ca.animate()

```
Animation controls
* Use `SPACE` to play/pause
* When paused, use `j/k` to step forward/back
* Use `r` to reverse time
* Use `0` to jump to the beginning, and `1-9` to skip around.

### What are multi-generational cellular automata?

There is a wonderful human named Mirek Wojtovicz who has done a lot of work to catalog and visualize lots of different types of cellular automata. His website is here: http://www.mirekw.com/
<br><br>
"Generations" is one of the many familites of CA rules that Mirek describes on his site. It's a simple extension of the familiar "Life" family of CAs which inclues Conway's Game of Life. Rather than transitioning from live to dead, cells enter a dying or refractory state where they are not counted as live cells but still take up space. This leads to highly dynamic evolution, often producing glider-like objects and other complex and aesthetically pleasing patters from shockingly simple rules.
<br><br>
Rules are encoded in strings with format 'S/B/G', where S = survival, B = birth, G = generations.
Game of Life is encoded as 23/3/2. G = 2 because there are only two states: alive and dead.
<br><br>
I scraped Mirek's website for a table of notable "Generations" rules with names and descriptions. You can view it as a pandas dataframe with `CA.rules_table`.
<br><br>

### Running a specific rule
You can pass a rule string or a rule name to the CA constructor.
```python
ca = CA(100, 100, rule='345/2/4')
```
345/2/4 is the rule for "Star Wars", one of the coolest CAs I've ever seen. The following is equivalent:
```python
ca = CA(100, 100, rule_name='Star Wars')
```
If both `rule` and `rule_name` are passed, `rule_name` is used.
### Display methods
A display method is a method that takes a game (3d numpy array) and an index, and draws a pattern on the pygame display as a function of the game and index. Passing a list of display method names to `display_methods` in the `animate()` function will cause those display methods to be used in that order.
<br><br>
Right now, the only ones that work are "generations" and "memory". "generations" draws a different color for each generation. "memory" adds up the past n frames and draws varying shades of red corresponding to the number for each cell.

### Cool Examples
Here are just a few examples of the incredible animations you can create with a multi-gen 2D CA and color map (a list of rgb tuples where the index corresponds to the state of the cell to which that color is assigned)

#### game of life with memory
```python
from ca2d import CA
gol = CA(100, 100)
gol.randomize()
gol.evolve(limit=1000)
gol.animate(display_methods=['memory', 'generations'], colors=[CA.Black, (102, 102, 102)])
```
![Game of Life with memory](/images/img1.png)
#### Brian's Brain with memory
```python
from ca2d import CA
bb = CA(100, 100, rule_name='Brian\'s Brain')
bb.randomize()
bb.evolve(limit=500)
bb.animate(display_methods=['memory', 'generations'])
```
![Brian's Brain with memory](/images/img2.png)
(Can you spot the Sierpinski triangles?)
#### Prairie on fire with fire colors
```python
from ca2d import CA
pf = CA(100, 100, rule_name='Prairie on fire')
pf.randomize(option='square')
pf.evolve(limit=500)
pf.animate(colors=CA.fire_colors)
```
![Prairie on fire with fire colors](/images/img3.png)
#### Meteor Guns
```python
from ca2d import CA
mg = CA(100, 100, rule_name='Meteor Guns')
mg.randomize(option='square', size=5)
mg.evolve(limit=500)
mg.animate(colors=CA.fire_colors)
```
![Meteor Guns with fire colors](/images/img4.png)
