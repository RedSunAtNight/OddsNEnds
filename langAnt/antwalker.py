#! usr/bin/env python
from numpy import zeros, ones
from matplotlib.pyplot import contourf, show

"""
antwalker.py
A little example of Langton's Ant.
@author: RedSunAtNight
"""
# Langton's Ant. An "ant" starts in the middle of a grid. 
# If it hits a square marked zero, the mark changes to 1 and the ant turns left.
# If it hits a square marked 1, the mark changes to zero and the ant turns right.
# If you let it go for enough steps, the ant eventually builds a highway.

gridSide = 150
grid = zeros((gridSide, gridSide))
# Number of steps for the ant to take.
maxN = 12000

# Initial position of the ant
position = [gridSide/2, gridSide/2]
# Initial direction the ant is facing. direction % 4 gives 0=up, 1=left, 2=down, 3=right
direction = 2 

# Function to handle the ant "turning" and moving
def turn_move(initPos, initDirec, turn, stepno): # For our purposes, turn will be either 1 or -1. stepno is for debugging.
	newdirection = (initDirec + turn) % 4
	if newdirection == 0:
		initPos[0] -= 1 # row number decreases, ant moves up one
	elif newdirection == 1:
		initPos[1] -= 1 # move to the left
	elif newdirection == 2:
		initPos[0] += 1 # move down
	elif newdirection == 3:
		initPos[1] += 1
	else:
		raise ValueError("Invalid direction-number at step {0}.".format(stepno))
	return (initPos, newdirection)

# Actually walking around the grid.
for step in range(0, maxN):
	if grid[position[0]][position[1]] == 0:
		grid[position[0]][position[1]] = 1
		position, direction = turn_move(position, direction, 1, step)
	elif grid[position[0]][position[1]] == 1:
		grid[position[0]][position[1]] = 0
		position, direction = turn_move(position, direction, -1, step)
	else:
		raise ValueError("Invalid value at grid position y={0}, x={1}; occurred during step {2}.".format(position[0], position[1], step))

# Let's see it
levels = [-0.5, 0.5, 1.5]
contourf(grid, levels, colors=('white','black'))
show()
		
