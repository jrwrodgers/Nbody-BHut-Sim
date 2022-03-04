import matplotlib.pyplot as plt
from random import random
from particle import Particle
from quadtree import QuadTree, Point, Rectangle
import numpy as np
import time
import math



width=10
height=10
nparticles=1000
particles=[]
scatter_array=np.zeros((nparticles,2))
qtree_rectangle=[]
DEBUG=False

def print_attrs(a):
    attrs = vars(a)
    print(', '.join("%s: %s" % item for item in attrs.items()))

def main():
    qtree_rectangle = Rectangle(0, 0, width, height)
 #   print_attrs(qtree_rectangle)
    qtree=QuadTree(qtree_rectangle, 5, 1)

    for __ in range(nparticles):
         pos=[random()*width-width/2,random()*height-height/2]
         vel=[0,0]
         particles.append(Particle(pos,vel,1,))
    # particles.append(Particle([1, 1], [0, 0], 1, 1))
    # particles.append(Particle([2, 2], [0, 0], 1, 1))
    # particles.append(Particle([3, 3], [0, 0], 1, 1))
    # particles.append(Particle([4, 4], [0, 0], 1, 1))

    for i in range(len(particles)):
        point=Point(particles[i].pos_x,particles[i].pos_y,particles[i].mass)
        if DEBUG:print("inserting point", i)
        qtree.insert_point(point,DEBUG)
        scatter_array[i, 0] = particles[i].pos_x
        scatter_array[i, 1] = particles[i].pos_y

    ## Plot points
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(8, 8), dpi=160)
    ax = plt.subplot()
    scatter1 = plt.scatter(scatter_array[:, 0], scatter_array[:, 1], s=10, color=[.7, .7, 1], alpha=0.3)
    if DEBUG:
        for i in range(len(particles)):
            ax.annotate(str(i), (scatter_array[i,0], scatter_array[i,1]))

    qtree.plot_rectangle(ax)

    fig.canvas.draw()
    plt.show()

    ## Plot Tree


if __name__ == '__main__':
    main()
