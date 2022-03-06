import matplotlib.pyplot as plt
from random import random
from particle import Particle
from quadtree import QuadTree, Point, Rectangle
import numpy as np
import time
import math



window_width = 8
nparticles = 3000
nlargebody = 5
capacity = 1
width = 4
height = 4
nt = 10
dt = 0.001
G = -0.5
eta = 0.05
theta = 0.5
QTREE_SHOW = False
DYNAMIC_TREE_LIMS = False
QTREE_PRINT = False
COFG_SHOW = False


##### CALL THIS AS FUNCTION WITH SETUP PARAMS - OUTPUT VECTORS OF POINTS AT EACH TIME STEP

def main():
    print("NBody Sim")
    particles = []
    tt = 0

    scatter_com = np.zeros((1, 2))
    qtree_rectangle = Rectangle(0, 0, width, height)
    qtree = QuadTree(qtree_rectangle, capacity, 1)

    # Create initial particle conditions
    start_vel = 20
    for i in range(nparticles-nlargebody):
        xpos = random() * width - width / 2
        ypos = random() * height - height / 2
        r = (xpos ** 2 + ypos ** 2) ** 0.5
        angle = math.atan2(ypos, xpos)
        thetanew = angle + math.pi / 2
        u = start_vel * math.cos(thetanew) / r
        v = start_vel * math.sin(thetanew) / r
        particles.append(Particle(position=[xpos, ypos], velocity=[u, v]))

    for i in range(nlargebody):
        xpos = random() * width - width / 2
        ypos = random() * height - height / 2
        r = (xpos ** 2 + ypos ** 2) ** 0.5
        angle = math.atan2(ypos, xpos)
        thetanew = angle + math.pi / 2
        u = start_vel * math.cos(thetanew) / r
        v = start_vel * math.sin(thetanew) / r
        particles.append(Particle(position=[xpos, ypos], velocity=[u, v], mass=100, radius=50))


    scatter_array = np.zeros((len(particles), 2))
    scatter_sizes = np.zeros((len(particles), 1))

    for i in range(len(particles)):
        scatter_array[i, 0] = particles[i].x
        scatter_array[i, 1] = particles[i].y
        scatter_sizes[i, 0] = particles[i].radius
        point = Point(particles[i].x, particles[i].y, particles[i].mass)
        qtree.insert_point(point)


    # Prep figures
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(window_width, window_width), dpi=160)
    ax1 = plt.subplot()
    scatter1 = plt.scatter(scatter_array[:, 0], scatter_array[:, 1], s=scatter_sizes[:, 0], color=[.7, .7, 1],
                           alpha=0.3, edgecolor='none')
    if COFG_SHOW == True:
        scatter2 = plt.scatter(scatter_com[:, 0], scatter_com[:, 1], s=40, color=[1, 0, 0], marker="+")
    ax1.set_aspect('equal', 'box')
    ax1.set(xlim=(-width, width), ylim=(-height, height))

    ### START TIME LOOP
    for tt in range(int(nt / dt)):
        qtree_start_time = time.time()

##Create QTREE

        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        # Dynamic size of quadtree
        if DYNAMIC_TREE_LIMS == True:
            new_width = max(abs(min_x), abs(max_x)) * 2
            new_height = max(abs(min_y), abs(max_y)) * 2
            new_max = max(new_width, new_height) * 1.01
            qtree_rectangle = Rectangle(0, 0, new_max, new_max)
            ax1.set(xlim=(-new_max, new_max), ylim=(-new_max, new_max))
        else:
            qtree_rectangle = Rectangle(0, 0, width, height)

        # Make new quadtree
        qtree = QuadTree(qtree_rectangle, capacity, 1)

        for particle in particles:
            point = Point(particle.x, particle.y, particle.mass)
            qtree.insert_point(point)

        CMx = qtree.cofg_x
        CMy = qtree.cofg_y
        scatter_com[0, 0] = CMx
        scatter_com[0, 1] = CMy

        ##Get Energies
        PE = 0
        for i in range(len(particles)):
            dist2CM = ((CMx - particles[i].x) ** 2 + (CMy - particles[i].y) ** 2) ** 0.5
            PE += particles[i].mass * (dist2CM ** 2)
            scatter_array[i, 0] = particles[i].x
            scatter_array[i, 1] = particles[i].y
            scatter_sizes[i, 0] = particles[i].radius

            if particles[i].x < min_x: min_x = particles[i].x
            if particles[i].x > max_x: max_x = particles[i].x
            if particles[i].y < min_x: min_y = particles[i].y
            if particles[i].y > max_y: max_y = particles[i].y

        KE = 0
        for particle in particles:
            KE += 0.5 * particle.mass * (particle.vel_x ** 2 + particle.vel_y ** 2)

        qtree_end_time = time.time()

        plot_start_time = time.time()

        ###### Draw plot
        scatter1.set_offsets(scatter_array)
        if COFG_SHOW == True:
            scatter2.set_offsets(scatter_com)

        ax1.patches = []
        if QTREE_SHOW:
            qtree.plot_rectangle(ax1)
        if QTREE_PRINT:
            qtree.output_tree()

        plot_end_time=time.time()
        tt += dt

        title_str = "Time elapsed =" + str(f'{tt * dt:.3f}') + " s"
        ax1.set_title(title_str)


        fig.canvas.draw()
        fig.canvas.flush_events()
        OTHER_SHOW=False

        ### PARALLELISE NEXT STEP
        ## NPROCS=4
        ## Split into 4 groups of particles

        process_start_time=time.time()
        for i in range(len(particles)):
            # if i==0: OTHER_SHOW =True
            # else: OTHER_SHOW = False
            #print("checking others for point ",i," X,Y =",particles[i].x,particles[i].y)
            others = (particles[i].get_theta_qtree(G, qtree, theta,ax1,OTHER_SHOW))
            #print("Others used :", len(others))
            particles[i].update_force(others, G, eta)
            #particles[i].update_force(particles, G, eta)

        for particle in particles:
            particle.update_pos(dt)
        process_end_time=time.time()
        ## END PARALLEL PHASE

        #print("Time =", str(f'{tt * dt:.3f}'), MT, str(f'{PE:.0f}'), str(f'{KE:.0f}'), str(f'{PE - KE:.0f}'))
        print("Time =",str(f'{tt * dt:.3f}'),"qtree time =", str(f'{(qtree_end_time-qtree_start_time)*1000:.3f}'),
            "plot time =",str(f'{(plot_end_time-plot_start_time)*1000:.3f}'),
            "proc time=",str(f'{(process_end_time-process_start_time)*1000:.3f}'))
        plt.pause(0.01)


if __name__ == '__main__':
    main()
