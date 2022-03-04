import matplotlib.pyplot as plt
from random import random
from particle import Particle
from quadtree import QuadTree, Point, Rectangle
import numpy as np
import time
import math


nparticles = 15
capacity = 2
width=4
height=4
nt=10
dt=0.001
G=-0.5
eta=0.05
theta=0.5
DEBUG=False
QTREE_SHOW = True



def main():
    print("NBody Sim")
    particles =[]
    tt=0
    scatter_array=np.zeros((nparticles,2))
    scatter_sizes=np.zeros((nparticles,1))
    scatter_com=np.zeros((1,2))
    qtree_rectangle = Rectangle(0, 0, width, height)
    qtree = QuadTree(qtree_rectangle, capacity, 1)

    start_vel=5
    for i in range(nparticles-1):
        xpos=random()*0.7*width-width/2
        ypos=random()*0.7*height-height/2
        r=(xpos**2+ypos**2)**0.5
        theta=math.atan2(ypos,xpos)
        thetanew=theta+math.pi/2
        u=start_vel*math.cos(thetanew)/r
        v=start_vel*math.sin(thetanew)/r
        particles.append(Particle(position=[ xpos, ypos ],velocity=[u,v]))
        scatter_array[i, 0]=particles[i].x
        scatter_array[i, 1] = particles[i].y
        scatter_sizes[i,0] = particles[i].radius
        point = Point(particles[i].x, particles[i].y, particles[i].mass)
        qtree.insert_point(point, DEBUG)

    particles.append(Particle(position=[0, 0], velocity=[0, 0], mass=1000, radius=50))
    qtree.insert_point(Point(0,0,30), DEBUG)


    #Prep figures
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(8, 7), dpi=100)
    grid = plt.GridSpec(4, 1, wspace=0.0, hspace=0.01)
    ax1 = plt.subplot(grid[0:3, 0])
    #ax2 = plt.subplot(grid[3, 0])
    scatter1=plt.scatter(scatter_array[:,0], scatter_array[:,1], s=scatter_sizes[:,0], color=[.7, .7, 1], alpha=0.3)
    scatter2=plt.scatter(scatter_com[:,0], scatter_com[:,1], s=40, color=[1, 0, 0], marker="+")
    ax1.set_aspect('equal', 'box')
    #ax1.set_xticks([-2, -1, 0, 1, 2])
    #ax1.set_yticks([-2, -1, 0, 1, 2])
    #ax1.set(xlim=(-width, width), ylim=(-height, height))


    for tt in range(int(nt/dt)):
        start_time = time.time()

        ##Create QTREE

        CMx = 0
        CMy = 0
        MT = 0
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0


        # Dynamic size of quadtree
        new_width = max(abs(min_x), abs(max_x)) * 2
        new_height = max(abs(min_y), abs(max_y)) * 2
        new_max = max(new_width, new_height) * 1.01
        # qtree_rectangle = Rectangle(0, 0, new_max, new_max)
        qtree_rectangle = Rectangle(0, 0, width, height)

        # Make new quadtree
        qtree = []
        qtree = QuadTree(qtree_rectangle, capacity, 1)
        scatter_com[0, 0] = CMx / MT
        scatter_com[0, 1] = CMy / MT

        ##Get Energies
        PE = 0
        for i in range(len(particles)):
            dist2CM = ((CMx - particles[i].x) ** 2 + (CMy - particles[i].y) ** 2) ** 0.5
            PE += particles[i].mass * (dist2CM ** 2)

            scatter_array[i, 0] = particles[i].x
            scatter_array[i, 1] = particles[i].y
            scatter_sizes[i, 0] = particles[i].radius
            point = Point(particles[i].x, particles[i].y, particles[i].mass)
            qtree.insert_point(point, DEBUG)
            CMx += particle.mass * particle.x
            CMy += particle.mass * particle.y
            MT += particle.mass
            if particle.x < min_x: min_x =particle.x
            if particle.x > max_x: max_x = particle.x
            if particle.y < min_x: min_y = particle.y
            if particle.y > max_y: max_y = particle.y

        KE = 0
        for particle in particles:
            KE += 0.5 * particle.mass * (particle.vel_x ** 2 + particle.vel_y ** 2)

        for particle in particles:
            others=particle.get_theta_qtree(G, qtree, theta)
            particle.update_force(others,G,eta)
            particle.update_force(particles, G, eta)

        for particle in particles:
            particle.update_pos(dt)






        ###### Draw plot
        scatter1.set_offsets(scatter_array)
        scatter2.set_offsets(scatter_com)
        #ax1.set(xlim=(-new_max, new_max), ylim=(-new_max, new_max))
        ax1.patches = []
        if QTREE_SHOW: qtree.plot_rectangle(ax1)
        #
        tt+=dt
        end_time=time.time()
        title_str="Time elapsed =" +str(f'{tt*dt:.3f}') + " s, Comp_dT: "+ str(f'{end_time-start_time:.4f}')
        ax1.set_title(title_str)
        print("Time =", str(f'{tt*dt:.3f}'), MT, str(f'{PE:.0f}'), str(f'{KE:.0f}'), str(f'{PE-KE:.0f}'))
        #
        #plt.sca(ax2)
        #plt.scatter(tt * dt, KE, s=1, color=[1, 0, 0], alpha=1)
        #plt.scatter(tt * dt, PE, s=1, color=[0, 1, 0], alpha=1)
        #plt.scatter(tt * dt, PE+KE, s=1, color=[0, 0, 1], alpha=1)
  #
        fig.canvas.draw()
        fig.canvas.flush_events()

        plt.pause(0.01)




if __name__ == '__main__':
    main()



