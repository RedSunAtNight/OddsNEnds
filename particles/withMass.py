#! usr/bin/env python
from math import sqrt
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

'''
withMass.py
A particle interaction in three dimensions.
@author: RedSunAtNight
@version: 1.0
Declares the Particle class. Particles can either attract or repel each other.
Makes three particles (called positron, electron, and elec2, but they are classical particles, not quantum ones) and sends them past each other. Animates their interaction.
Requires:
Everything imported above.

This uses Verlet integration to make the particles' trajectories. The difference between this simulation and interaction_Verlet.py is that the particles now have a mass attribute, which affects their kinematics.

Issues:
    At least on my machine, rotating the animated figure causes the axes to be relabeled, so the the x-, y-, and z-labels are always in the same position, regardless of how the graph is actually oriented. This is less than helpful.

Nice-looking example:
Two particles, one positive (mass 25) and one negative (mass 1).
positive init position: [-3., 1., 0], init velocity: [0, 1., 0]
negative init position: [3., -1., 0], init velocity: [0, -1., 0]
The positive particle moves in almost a straight line, with small kinks in it.
The negative one "curlicues" its way around the positive one, following it.

If, instead, the positive one starts with a velocity of zero, the negaitve one shoots toward it, goes around it, and flies off away.
The positive one will approach the negative one slightly, and then also go away from it.
'''

class Particle:
    kind = ""
    mass = 5.
    position = [0, 0, 0]
    prevposition = [0, 0, 0]
    initvelocity = [0, 0, 0]
    acceleration = [0, 0, 0]
    stepno = 0 # keep track of how many timesteps the particle has taken.

    # xDist and yDist point from the particle being acted on to the particle causing the force.
    # so, to find the acceleration of particle 1 due to particle 2, you would use x2-x1 and y2-y1.
    def attractAccel(self, distvec):
        # inverse-square law
        sqrDist = distvec[0]**2 + distvec[1]**2 + distvec[2]**2
        # acceleration is force/mass. Currently, particle mass doesn't affect the strength of the force.
        accel = (125. / sqrDist) / self.mass
        xComp = accel * distvec[0] / sqrt(sqrDist)
        yComp = accel * distvec[1] / sqrt(sqrDist)
        zComp = accel * distvec[2] / sqrt(sqrDist)
        return [xComp, yComp, zComp]

    def repelAccel(self, distvec):
        [negex, negy, negz] = self.attractAccel(distvec)
        return [-1*negex, -1*negy, -1*negz]

    # gives the acceleration of this particle caused by the presence of another particle
    def interact(self, listOtherPartls):
        accel = [0, 0, 0]
        for otherPartl in listOtherPartls:
            distancevec = [otherPartl.position[0] - self.position[0], otherPartl.position[1] - self.position[1], otherPartl.position[2] - self.position[2]]
            if otherPartl.kind == self.kind:
                accel[0] += self.repelAccel(distancevec)[0]
                accel[1] += self.repelAccel(distancevec)[1]
                accel[2] += self.repelAccel(distancevec)[2]
            else: 
                accel[0] += self.attractAccel(distancevec)[0]
                accel[1] += self.attractAccel(distancevec)[1]
                accel[2] += self.attractAccel(distancevec)[2]
        self.acceleration = accel

    # gives the particle's new velocity and position, based on the acceleration. Uses Verlet integration.
    def move(self, timestep):
        self.stepno += 1
        if self.stepno == 1:
            # No choice but to Taylor-expand this; Verlet integration requires an x(t - dt) position.
            newX = self.position[0] + self.initvelocity[0]*timestep + 0.5*self.acceleration[0]*timestep**2
            newY = self.position[1] + self.initvelocity[1]*timestep + 0.5*self.acceleration[1]*timestep**2
            newZ = self.position[2] + self.initvelocity[2]*timestep + 0.5*self.acceleration[2]*timestep**2
            self.prevposition = self.position
            self.position = [newX, newY, newZ]
        elif self.stepno > 1:
            # Verlet Integration. x(t+dt) = 2x(t) - x(t-dt) + a(t)dt^2 + O(dt^4)
            newX = (2 * self.position[0]) - self.prevposition[0] + self.acceleration[0]*timestep**2
            newY = (2 * self.position[1]) - self.prevposition[1] + self.acceleration[1]*timestep**2
            newZ = (2 * self.position[2]) - self.prevposition[2] + self.acceleration[2]*timestep**2
            self.prevposition = self.position
            self.position = [newX, newY, newZ]
        else:
            raise RuntimeError('At step {0}: this stepno is invalid.'.format(self.stepno))

# A function for updating the plot of the particles' trajectory:
def update_path(num, listPlots, listDatas):
    if len(listDatas) != len(listPlots):
        raise IndexError('Funtion update_path - Must have same number of plots as datasets (len(listDatas) must == len(listPlots)).')
    else:
        for i in range(0, len(listPlots)):
            listPlots[i].set_data(listDatas[i][0][0:update_path.skipover*num], listDatas[i][1][0:update_path.skipover*num])
            listPlots[i].set_3d_properties(listDatas[i][2][0:update_path.skipover*num])
    return listPlots
update_path.skipover = 5 # to keep the animation from being painfully slow


# Initialize two particles of different kinds:
electron = Particle()
electron.kind = "negative"
electron.mass = 1.
electron.position = [3., -1., 0] # Good starting point for only two particles: [3., -1.]
electron.initvelocity = [0, -1., 0] # Good starting velocity: [0, -1.]
positron = Particle()
positron.kind = "positive"
positron.mass = 25.
positron.position = [-3., 1., 0] # Good starting point for only two particles: [-3., 1.]
positron.initvelocity = [0, 1., 0] # Good starting velocity: [0, 1.]
# These'll hold position information for the electron and positron
elecpos = [[electron.position[0]],[electron.position[1]], [electron.position[2]]]
pospos = [[positron.position[0]],[positron.position[1]], [positron.position[2]]]

# Let's introduce another:
# Comment out this particle and all references to it below to see a nice example of two particles orbiting each other.
#elec2 = Particle()
#elec2.kind = "negative"
#elec2.position = [0.0, 0.0, -3.5]
#elec2.initvelocity = [0., 0.0, 0.0]
#twopos = [[elec2.position[0]], [elec2.position[1]], [elec2.position[2]]]


timeaxis = [0]
dTime = 0.01 # at size 0.1 it starts to spiral out a little bit
maxTime = 1000 # steps for same path distance as Taylor: 200

for j in range(1, maxTime):
    timeaxis.append(j*dTime)
    electron.interact([positron])
    positron.interact([electron])
    #elec2.interact([electron, positron])
    electron.move(dTime)
    positron.move(dTime)
    #elec2.move(dTime)
    elecpos[0].append(electron.position[0])
    elecpos[1].append(electron.position[1])
    elecpos[2].append(electron.position[2])
    pospos[0].append(positron.position[0])
    pospos[1].append(positron.position[1])
    pospos[2].append(positron.position[2])
    #twopos[0].append(elec2.position[0])
    #twopos[1].append(elec2.position[1])
    #twopos[2].append(elec2.position[2])

fig = plt.figure()
ax = p3.Axes3D(fig)


pathElec, = ax.plot([], [], [], 'r-')
pathPos, = ax.plot([], [], [], 'b-')
#pathTwo, = plt.plot([], [], [], 'g-')


aniElec = animation.FuncAnimation(fig, update_path, len(elecpos[0])/update_path.skipover, fargs=([pathElec, pathPos], [elecpos, pospos]), interval=0.01, blit=True)

ax.set_xlim3d([-4.0, 4.0])
ax.set_xlabel('x')

ax.set_ylim3d([-4.0, 4.0])
ax.set_ylabel('y')

ax.set_zlim3d([-4.0, 4.0])
ax.set_zlabel('z')

ax.set_title('Particle interaction')

aniElec.save('spirals.ogg')

plt.show()
