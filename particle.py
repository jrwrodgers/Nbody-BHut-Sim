import functions

class Particle:
    def __init__(self, position = [0.0,0.0], velocity = [0.0,0.0], mass = 1.0, radius=1.0):
        self.pos_x = position[0]
        self.pos_y = position[1]
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
        f_tot=[]
        f_tot.append(0)
        f_tot.append(0)

        for other in others:
            if other !=self:
                dx=self.pos_x-other.pos_x
                dy=self.pos_y-other.pos_y
                distance_softened=((dx)**2+(dy)**2+eta**2)**1.5
                #theta=math.atan(-1*dy/dx)
                fx = dx * G * self.mass * other.mass / distance_softened
                fy = dy * G * self.mass * other.mass / distance_softened
                f_tot[0]+=fx
                f_tot[1]+=fy
        #print(f_tot)
        return f_tot[0], f_tot[1]

    def update_force(self,others,G,eta):
        self.acc_new_x, self.acc_new_y  = self.calc_attractions(others, G, eta)


    def update_pos(self,dt):
        # 0.5 kick
        self.vel_x += self.acc_old_x * dt * 0.5
        self.vel_y += self.acc_old_y * dt * 0.5
        # drift
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        # 0.5 kick
        self.vel_x += self.acc_new_x * dt * 0.5
        self.vel_y += self.acc_new_y * dt * 0.5
        #swap
        self.acc_old_x=self.acc_new_x
        self.acc_old_y = self.acc_new_y