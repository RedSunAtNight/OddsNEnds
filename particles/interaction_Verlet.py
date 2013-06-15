#! usr/bin/env python
from math import sqrt
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

'''
interaction_Verlet.py
A particle interaction in three dimensions.
@author: RedSunAtNight
@version: 1.0
Declares the Particle class. Particles can either attract or repel each other.
Makes three particles (called positron, electron, and elec2, but they are classical particles, not quantum ones) and sends them past each other. Animates their interaction.
Requires:
Everything imported above.

Difference between this and interaction_Taylor version:
    Integrates the motion using Verlet integration, except on the first timestep.
    Adds the fields "stepno" and "prevposition" to the Particle class.

Issues:
    At least on my machine, rotating the animated figure causes the axes to be relabeled, so the the x-, y-, and z-labels are always in the same position, regardless of how the graph is actually oriented. This is less than helpful.
'''

class Particle:
    kind = ""
    position = [0, 0, 0]
    prevposition = [0, 0, 0]
    initvelocity = [0, 0, 0]
    velocity = [0, 0, 0]
    acceleration = [0, 0, 0]
    stepno = 0 # keep track of how many timesteps the particle has taken.

    # xDist and yDist point from the particle being acted on to the particle causing the force.
    # so, to find the acceleration of particle 1 due to particle 2, you would use x2-x1 and y2-y1.
    # distvec must be the same dimensionality as position, velocity, and acceleration
    def attractAccel(self, distvec):
        # inverse-square law
        sqrDist = 0
        result = []
        for dimension in distvec:
            sqrDist += dimension**2
        accel = 25. / sqrDist
        for i in range(0, len(distvec)):
            result.append(accel * distvec[i] / sqrt(sqrDist));
        return result

    def repelAccel(self, distvec):
        negresult = self.attractAccel(distvec)
        result = []
        for comp in negresult:
            result.append(-1*comp);
        return result

    # gives the acceleration of this particle caused by the presence of another particle
    def interact(self, listOtherPartls):
        accel = [0] * self.position.length
        for otherPartl in listOtherPartls:
            distancevec = []
            for j in range(0, self.position.length):
                distancevec.append(otherPartl.position[i] - self.position[i])
            if otherPartl.kind == self.kind:
                for i in range(0, distancevec.length):
                    accel[i] += self.repelAccel(distancevec)[i]
            else: 
                for i in range(0, distancevec.length):
                    accel[i] += self.attractAccel(distancevec)[i]
        self.acceleration = accel

    # gives the particle's new velocity and position, based on the acceleration. Uses Verlet integration.
    def move(self, timestep):
        self.stepno += 1
        if self.stepno == 1:
            # No choice but to Taylor-expand this; Verlet integration requires an x(t - dt) position.
            self.prevposition = self.position
            for i in range(0, self.position.length):
                self.position[i] = self.position[i] + self.initvelocity[i]*timestep + 0.5*self.acceleration[i]*timestep**2
                self.velocity[i] = self.velocity + self.acceleration[i]*timestep
        elif self.stepno > 1:
            tempPosition = self.position
            for i in range(0, self.position.length):
                # Verlet Integration. x(t+dt) = 2x(t) - x(t-dt) + a(t)dt^2 + O(dt^4)
                self.position[i] = (2 * self.position[i]) - self.prevposition[i] + self.acceleration[i]*timestep**2
                # at least loosely keep track of velocity
                self.velocity[i] = self.velocity + self.acceleration[i]*timestep
            self.prevposition = tempPosition
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
update_path.skipover = 1 # to keep the animation from being painfully slow

if __name__ == "__main__":
    # Initialize two particles of different kinds:
    electron = Particle()
    electron.kind = "negative"
    electron.position = [3., -1., 0] # Good starting point for only two particles: [3., -1.]
    electron.initvelocity = [0, -1., 0] # Good starting velocity: [0, -1.]
    positron = Particle()
    positron.kind = "positive"
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
    dTime = 0.05 # at size 0.1 it starts to spiral out a little bit
    maxTime = 200 # steps for same path distance as Taylor: 200
    '''
    using dTime = 0.05 and maxTime = 200,
    the actual time required to run the simulation and build the
    animation, but not show it:
    real	0m29.876s
    user	0m29.246s
    sys	0m0.452s
    and trying again
    real	0m28.268s
    user	0m27.750s
    sys	0m0.392s
    '''
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
    
    aniElec.save('ellipsesVerlet.ogg')
    
    plt.show()
