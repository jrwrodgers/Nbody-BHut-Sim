import functions

class Particle:
    def __init__(self, position = [0.0,0.0], velocity = [0.0,0.0], mass = 1.0, radius=5.0):
        self.x = position[0]
        self.y = position[1]
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]
        self.acc_old_x = 0.0
        self.acc_old_y = 0.0
        self.acc_new_x = 0.0
        self.acc_new_y = 0.0
        self.mass = mass
        self.radius = radius
        self.highlighted= False

    def calc_attractions(self,others,G,eta):
        a_tot=[]
        a_tot.append(0)
        a_tot.append(0)

        for other in others:
            if other !=self:
                dx=self.x-other.x
                dy=self.y-other.y
                distance_softened=(((dx)**2+(dy)**2)**0.5+eta)**2
                #theta=math.atan(-1*dy/dx)
                ax = dx * G * other.mass / distance_softened
                ay = dy * G * other.mass / distance_softened
                a_tot[0]+=ax
                a_tot[1]+=ay
        #print(f_tot)
        return a_tot[0], a_tot[1]

    def update_force(self,others,G,eta):
        self.acc_new_x, self.acc_new_y  = self.calc_attractions(others, G, eta)

    def get_theta_qtree(self,G,qt,theta):
        others=[]
        others.append(qt.theta_bounds(theta,Point(self.x,self.y,self.mass)),others)
        print(len(others))
        #update_force(others, G, eta)
        return others

    def update_pos(self,dt):
        # 0.5 kick
        self.vel_x += self.acc_old_x * dt * 0.5
        self.vel_y += self.acc_old_y * dt * 0.5
        # drift
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        # 0.5 kick
        self.vel_x += self.acc_new_x * dt * 0.5
        self.vel_y += self.acc_new_y * dt * 0.5
        #swap
        self.acc_old_x=self.acc_new_x
        self.acc_old_y = self.acc_new_y