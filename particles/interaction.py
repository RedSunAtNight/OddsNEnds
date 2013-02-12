#! usr/bin/env python
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy

'''
interaction.py
A particle interaction in two dimensions.
@author: Helenka Casler
@version: 1.0
Declares the Particle class.
Makes two particles (called positron and electron, but they are classical particles, not quantum ones) and sends them past each other. Animates their interaction.
'''

class Particle:
	kind = ""
	position = [0, 0]
	velocity = [0, 0]
	acceleration = [0, 0]

	# xDist and yDist point from the particle being acted on to the particle causing the force.
	# so, to find the acceleration of particle 1 due to particle 2, you would use x2-x1 and y2-y1.
	def attractAccel(self, distvec):
		# inverse-square law
		sqrDist = distvec[0]**2 + distvec[1]**2
		accel = 25. / sqrDist
		xComp = accel * distvec[0] / sqrt(sqrDist)
		yComp = accel * distvec[1] / sqrt(sqrDist)
		return [xComp, yComp]

	def repelAccel(self, distvec):
		[negex, negy] = attractAccel(distvec)
		return [-1*negex, -1*negy]

	# gives the acceleration of this particle caused by the presence of another particle
	def interact(self, particleObj):
		distancevec = [particleObj.position[0] - self.position[0], particleObj.position[1] - self.position[1]]
		if particleObj.kind == self.kind:
			self.acceleration = self.repelAccel(distancevec)
		else : self.acceleration = self.attractAccel(distancevec)

	def move(self, timestep):
		newX = self.position[0] + self.velocity[0]*timestep + 0.5*self.acceleration[0]*timestep**2
		newY = self.position[1] + self.velocity[1]*timestep + 0.5*self.acceleration[1]*timestep**2
		self.position = [newX, newY]
		newVx = self.velocity[0] + self.acceleration[0]*timestep
		newVy = self.velocity[1] + self.acceleration[1]*timestep
		self.velocity = [newVx, newVy]

# Initialize two particles of different kinds:
electron = Particle()
electron.kind = "negative"
electron.position = [3., -1.]
electron.velocity = [0, -1.]
positron = Particle()
positron.kind = "positive"
positron.position = [-3., 1.]
positron.velocity = [0, 1.]
# These'll hold position information for the electron and positron
elecpos = [[electron.position[0]],[electron.position[1]]]
pospos = [[positron.position[0]],[positron.position[1]]]

timeaxis = [0]
dTime = 0.0001
maxTime = 100000
for j in range(1, maxTime):
	timeaxis.append(j*dTime)
	electron.interact(positron)
	positron.interact(electron)
	electron.move(dTime)
	positron.move(dTime)
	elecpos[0].append(electron.position[0])
	elecpos[1].append(electron.position[1])
	pospos[0].append(positron.position[0])
	pospos[1].append(positron.position[1])



fig = plt.figure()
plt.title('Particle interaction in two dimensions')
plt.xlim(-3.2, 3.2)
plt.ylim(-3.2, 3.2)
plt.xlabel('x')
plt.ylabel('y')
pathElec, = plt.plot([], [], 'r-')
pathPos, = plt.plot([], [], 'b-')

# Now, to animate our particles:
skipover = 90 # to keep the animation from being painfully slow
def update_path(num, data1, aplot1, data2, aplot2):
	aplot1.set_data(data1[0][0:skipover*num], data1[1][0:skipover*num])
	aplot2.set_data(data2[0][0:skipover*num], data2[1][0:skipover*num])
	return aplot1, aplot2

aniElec = animation.FuncAnimation(fig, update_path, numpy.arange(1, len(elecpos[0]) / skipover), fargs=(elecpos, pathElec, pospos, pathPos), interval=0.01, blit=True)

plt.show()

