from math import sqrt

'''
particleClasses.py
@author: RedSunAtNight

class Particle
    Has charge, mass, position, acceleration, and a force constant. Also holds its own previous position, and its initial velocity.
    The force constant is analogous to the gravitational constant G, or the electrostatic constant 1/4*pi*epsilon.

class Gravitator(Particle)
    Must be initialized with a mass. May also get a position as a second argument.
    Force constant is G = 6.674 * 10**(-11) m^3 / kg*s^2.
    Throws an error if two particles with different charges try to interact.
    
    TODO: add particle radius and collisions.
'''

#   Particle
#   Base class for Gravitator
class Particle:
    charge = ""
    mass = 5.
    position = [0, 0, 0]
    prevposition = [0, 0, 0]
    initvelocity = [0, 0, 0]
    acceleration = [0, 0, 0]
    stepno = 0 # keep track of how many timesteps the particle has taken.
    forceConst = 125.

    # xDist and yDist point from the particle being acted on to the particle causing the force.
    # so, to find the acceleration of particle 1 due to particle 2, you would use x2-x1 and y2-y1.
    def attractAccel(self, distvec):
        # inverse-square law
        sqrDist = distvec[0]**2 + distvec[1]**2 + distvec[2]**2
        # acceleration is force/mass. Currently, particle mass doesn't affect the strength of the force.
        accel = (self.forceConst / sqrDist) / self.mass
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
            if otherPartl.charge == self.charge:
                toAdd = self.repelAccel(distancevec)
                for i in range(0, 3):
                    accel[i] += toAdd[i]
            else: 
                toAdd = self.attractAccel(distancevec)
                for i in range(0, 3):
                accel[i] += toAdd[i]
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

#   Gravitator
#   Behaves according to the laws of Newtonian gravitation
#   Must be initialized with mass
#   Assumes SI units
#   Strict; no anti-mass allowed here. To do that stuff, make a plain Particle.
class Gravitator(Particle):
    def __init__(self, mass, position=[0,0,0]):
        super(Gravitator, self).__init__()
        self.mass = abs(mass)
        self.position = position
        self.charge = "grav"
        self.forceConst = 6.674 * 10**(-11) # in m^3 / kg*s^2

    def attractAccel(self, distvec, otherMass):
        # inverse-square law
        sqrDist = distvec[0]**2 + distvec[1]**2 + distvec[2]**2
        # acceleration is force/mass. Currently, particle mass doesn't affect the strength of the force.
        accel = (self.forceConst * otherMass / sqrDist)
        xComp = accel * distvec[0] / sqrt(sqrDist)
        yComp = accel * distvec[1] / sqrt(sqrDist)
        zComp = accel * distvec[2] / sqrt(sqrDist)
        return [xComp, yComp, zComp]

    def interact(self, listOtherPartls):
        accel = [0, 0, 0]
        for otherPartl in listOtherPartls:
            distancevec = [otherPartl.position[0] - self.position[0], otherPartl.position[1] - self.position[1], otherPartl.position[2] - self.position[2]]
            if otherPartl.charge == self.charge:
                toAdd = self.attractAccel(distancevec, otherPartl.mass)
                for i in range(0, 3):
                    accel[i] += toAdd[i]
            else: 
                raise RuntimeError('Gravitational \"charges\" cannot be different. Charges are given as {0} and {1}.'.format(self.charge, otherPartl.charge))
        self.acceleration = accel
