import matplotlib.pyplot as plt
from random import random
from particle import Particle
import time


nparticles = 100
width=2
height=2
nt=10
dt=0.01
G=-1.0
eta=0.1



def main():
    print("NBody Sim")
    particles =[]
    tt=0

    start_vel=0
    for _ in range(nparticles):
        particles.append(Particle(position=[random()*width-width/2 , random()*height-height/2],velocity=[(random()-0.5)*start_vel,(random()-0.5)*start_vel]))


    #Prep figures
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(8, 8), dpi=160)
    grid = plt.GridSpec(4, 1, wspace=0.0, hspace=0.01)
    ax1 = plt.subplot(grid[0:3, 0])
    ax2 = plt.subplot(grid[3, 0])


    for tt in range(int(nt/dt)):
        start_time = time.time()
        xx=[]
        yy=[]

        # for i in range(len(particles)):
        #    print(i, particles[i].pos_x, particles[i].pos_y, particles[i].vel_x, particles[i].vel_y, particles[i].acc_old_x,
        #       particles[i].acc_old_y)

        for particle in particles:
            particle.update_force(particles,G,eta)
            #print(particle.calc_attractions(particles,G,eta))
        CMx = 0
        CMy = 0
        MT = 0
        for particle in particles:
            particle.update_pos(dt)
            CMx += particle.mass * particle.pos_x
            CMy += particle.mass * particle.pos_y
            MT += particle.mass

        CMx = CMx / MT
        CMy = CMy / MT
        #print(MT)

        PE = 0
        for i in range(len(particles)):
            dist2CM = ((CMx-particles[i].pos_x)**2+(CMy-particles[i].pos_y)**2)**0.5
            PE+=particles[i].mass*(dist2CM**2)
            xx.append(particles[i].pos_x)
            yy.append(particles[i].pos_y)
         #   aa.append((particles[i].acc_new_x**2+particles[i].acc_new_y**2)**0.5)

        #alphas = np.interp(aa, [0, 1000], [0, 1]).tolist()

        ##Get Energies
        KE=0
        for particle in particles:
            KE+=0.5*particle.mass*(particle.vel_x**2+particle.vel_y**2)

        #print(MT,PE,KE,KE-PE)

        ###### Draw plot
        plt.sca(ax1)
        plt.cla()
        plt.scatter(xx, yy, s=1, color=[.7, .7, 1],alpha=0.3)
        plt.scatter(CMx,CMy,s=5, color=[1,0,0])
        tt+=dt
        end_time=time.time()
        title_str="Time elapsed =" +str(f'{tt*dt:.3f}') + " s, Comp_dT: "+ str(f'{end_time-start_time:.4f}')
        ax1.set_title(title_str)
        ax1.set_aspect('equal', 'box')
        ax1.set_xticks([-2, -1, 0, 1, 2])
        ax1.set_yticks([-2, -1, 0, 1, 2])
        ax1.set(xlim=(-width, width), ylim=(-height, height))


        plt.sca(ax2)
        plt.scatter(tt * dt, KE, s=1, color=[1, 0, 0], alpha=1)
        plt.scatter(tt * dt, PE, s=1, color=[0, 1, 0], alpha=1)
        #plt.scatter(tt * dt, PE+KE, s=1, color=[0, 0, 1], alpha=1)
  #
        fig.canvas.draw()
        plt.pause(0.00001)
        fig.canvas.flush_events()



if __name__ == '__main__':
    main()



