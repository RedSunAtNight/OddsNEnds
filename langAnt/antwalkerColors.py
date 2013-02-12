#! usr/bin/env python
from numpy import zeros, ones
from matplotlib.pyplot import contourf, show

"""
antwalkerColors.py
Four-color Langton's Ant.
@author: RedSunAtNight
"""

# Langton's Ant, slightly modified with pretty colors. An "ant" starts in the middle of a grid. 
# If it hits a square marked zero, the mark changes to 1 and the ant turns left.
# If it hits a square marked 1, the mark changes to zero and the ant turns right.
# If you let it go for enough steps, the ant eventually builds a highway.

gridSide = 150
grid = zeros((gridSide, gridSide))
# Number of steps for the ant to take.
maxN = 5900

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

# Actually walking around the grid. Two new colors have been added.
for step in range(0, maxN):
	if grid[position[0]][position[1]] == 0:
		grid[position[0]][position[1]] = 1
		position, direction = turn_move(position, direction, 1, step) # Turn left, move one
	elif grid[position[0]][position[1]] == 1:
		grid[position[0]][position[1]] = 2
		position, direction = turn_move(position, direction, -1, step) # Turn right, move one
	elif grid[position[0]][position[1]] == 2:
		grid[position[0]][position[1]] = 3
		position, direction = turn_move(position, direction, 0, step) # Step forward without turning
		position, direction = turn_move(position, direction, 1, step) # Then turn left and move one
	elif grid[position[0]][position[1]] == 3:
		grid[position[0]][position[1]] = 0
		position, direction = turn_move(position, direction, 2, step) # Turn around and move one
		position, direction = turn_move(position, direction, -1, step) # Turn right, move one
	else:
		raise ValueError("Invalid value at grid position y={0}, x={1}; occurred during step {2}.".format(position[0], position[1], step))

# Let's see it
levels = [-0.5, 0.5, 1.5, 2.5, 3.5]
contourf(grid, levels, colors=('blue','green', 'yellow', 'red'))
show()
		
