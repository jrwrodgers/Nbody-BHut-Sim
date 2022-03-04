from matplotlib import patches
import matplotlib.pyplot as plt

def print_attrs(a):
    attrs = vars(a)
    print(', '.join("%s: %s" % item for item in attrs.items()))


class QuadTree:
    def __init__(self, rectangle, capacity, level):
        self.rectangle = rectangle
        self.capacity = capacity
        self.cofg_x = 0.0
        self.cofg_y = 0.0
        self.cofg_mx = 0.0
        self.cofg_my = 0.0
        self.mass = 0.0
        self.divided = False
        self.points = []
        self.npoints=len(self.points)
        self.northeast = []
        self.southeast = []
        self.southwest = []
        self.northwest = []
        self.level=level


    def insert_point(self,point,DEBUG):

        if self.rectangle.contains(point):
            if len(self.points) < self.capacity and self.divided == False:
                self.points.append(point)
                self.add_node_mass(point)

                if DEBUG:print("inserted point at level ", self.level)

            elif len(self.points) == self.capacity and self.divided == False:
                if DEBUG:print("dividing..")
                self.points.append(point)
                self.add_node_mass(point)
                self.subdivide()
                for old_point in self.points:
                    if DEBUG:print("trying ne")
                    self.northeast.insert_point(old_point,DEBUG)
                    if DEBUG:print("trying se")
                    self.southeast.insert_point(old_point,DEBUG)
                    if DEBUG:print("trying sw")
                    self.southwest.insert_point(old_point,DEBUG)
                    if DEBUG:print("trying nw")
                    self.northwest.insert_point(old_point,DEBUG)
                self.points = []
            elif self.divided == True:
                self.points.append(point)
                self.add_node_mass(point)
                if DEBUG:print("trying ne")
                self.northeast.insert_point(point,DEBUG)
                if DEBUG:print("trying se")
                self.southeast.insert_point(point,DEBUG)
                if DEBUG:print("trying sw")
                self.southwest.insert_point(point,DEBUG)
                if DEBUG:print("trying nw")
                self.northwest.insert_point(point,DEBUG)
        else:
            return

    def subdivide(self):
        self.divided = True
        ne_rectangle = Rectangle(self.rectangle.centre_x + self.rectangle.width / 4,
                                 self.rectangle.centre_y + self.rectangle.height / 4,
                                 self.rectangle.width / 2, self.rectangle.height / 2)
        se_rectangle = Rectangle(self.rectangle.centre_x + self.rectangle.width / 4,
                                 self.rectangle.centre_y - self.rectangle.height / 4,
                                 self.rectangle.width / 2, self.rectangle.height / 2)
        sw_rectangle = Rectangle(self.rectangle.centre_x - self.rectangle.width / 4,
                                 self.rectangle.centre_y - self.rectangle.height / 4,
                                 self.rectangle.width / 2, self.rectangle.height / 2)
        nw_rectangle = Rectangle(self.rectangle.centre_x - self.rectangle.width / 4,
                                 self.rectangle.centre_y + self.rectangle.height / 4,
                                 self.rectangle.width / 2, self.rectangle.height / 2)
        self.northeast = QuadTree(ne_rectangle, self.capacity, self.level + 1)
        self.southeast = QuadTree(se_rectangle, self.capacity, self.level + 1)
        self.southwest = QuadTree(sw_rectangle, self.capacity, self.level + 1)
        self.northwest = QuadTree(nw_rectangle, self.capacity, self.level + 1)

    def add_node_mass(self,point):
        self.mass += point.mass
        self.cofg_mx += (point.x * point.mass)
        self.cofg_my += (point.y * point.mass)
        self.cofg_x = self.cofg_mx / self.mass
        self.cofg_y = self.cofg_my / self.mass
        self.npoints = len(self.points)


    def plot_rectangle(self,ax):
        cm = plt.get_cmap('gist_rainbow')
        ncolors=12
        cmi=[]
        for i in range(ncolors):
            cmi.append(cm(i//3*3.0/ncolors))
        for i in range(10):
            cmi.append(cm(6//3*3.0/ncolors))

        if self.divided == True:
            ax.add_patch(patches.Rectangle((self.rectangle.left, self.rectangle.lower), self.rectangle.width,
                                           self.rectangle.height, edgecolor=cmi[self.level],
                                           facecolor='none', linewidth=1))
            #ax.add_patch(patches.Circle((self.cofg_x, self.cofg_y), radius=self.rectangle.width / 10, facecolor='none',
            #                               edgecolor=cmi[self.level]))
            self.northeast.plot_rectangle(ax)
            self.southeast.plot_rectangle(ax)
            self.southwest.plot_rectangle(ax)
            self.northwest.plot_rectangle(ax)

        if self.divided == False and len(self.points)!=0:
            ax.add_patch(patches.Rectangle((self.rectangle.left, self.rectangle.lower), self.rectangle.width, self.rectangle.height, edgecolor=cmi[self.level],
                                           facecolor='none', linewidth=1))
            ax.add_patch(patches.Circle((self.cofg_x,self.cofg_y),radius=self.rectangle.width/10,facecolor='none',edgecolor='green'))
            for connect in self.points:
                dx=self.cofg_x-connect.x
                dy=self.cofg_y-connect.y
                ax.add_patch(patches.Arrow(connect.x,connect.y,dx,dy,width=0.001, edgecolor='green'))

        if self.divided == False and len(self.points) == 0:
            ax.add_patch(patches.Rectangle((self.rectangle.left, self.rectangle.lower), self.rectangle.width,
                                           self.rectangle.height, edgecolor=cmi[self.level],
                                           facecolor='none', linewidth=1))

    def theta_bounds(self,theta,point,others):
        dist=((self.cofg_x-point.x)**2+(self.cog_y-point.y)**2)**0.5
        check_theta=dist/self.rectangle.width

        if theta<=check_theta:
        #
        #
        # elif:
        #
        # else:

        others.append(self.northeast.theta_bounds(theta, point))
        others.append(self.southeast.theta_bounds(theta, point))
        others.append(self.southwest.theta_bounds(theta, point))
        others.append(self.northwest.theta_bounds(theta, point))

        return others
    # Start at root node
    # If this is an internal node (e.g. not divided) add force
    # Check children
    # Calculate theta of children
    # If below theta then add force
    # If not drop into child and repeat



class Point:
    def __init__(self,x,y,m):
        self.x=x
        self.y=y
        self.mass=m


class Rectangle:
    def __init__(self,centre_x,centre_y,width,height):
        self.centre_x=centre_x
        self.centre_y=centre_y
        self.width=width
        self.height=height
        self.left = centre_x - width/2
        self.right = centre_x + width/2
        self.lower = centre_y - height/2
        self.upper = centre_y + height/2

    def draw(self):
        lines=[0,0,0,0]
        return lines

    def contains(self,point):
        if point.x < self.right and point.x > self.left and point.y < self.upper and point.y > self.lower:
            return True
        else:
            return False