import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.tri as trian
import chaospy

class Delaunay:


    def __init__(self, center=(0, 0), radius=9999):
        center = np.asarray(center)
        # Краї рамки (для краси виводу, нічо до методу не має)
        self.coords = [center+radius*np.array((-1, -1)),
                       center+radius*np.array((+1, -1)),
                       center+radius*np.array((+1, +1)),
                       center+radius*np.array((-1, +1))]

        # Два словники для збереження трикутників і кіл, описаних навколо них
        self.triangles = {}
        self.circles = {}

        # Два початкові трикутники (проти годинникової стрілки)
        T1 = (0, 1, 3)
        T2 = (2, 3, 1)
        self.triangles[T1] = [T2, None, None]
        self.triangles[T2] = [T1, None, None]

        # Обчислюємо описане коло навколо кожного трикутника
        for t in self.triangles:
            self.circles[t] = self.circumcenter(t)

    def circumcenter(self, tri):
        pts = np.asarray([self.coords[v] for v in tri])
        pts2 = np.dot(pts, pts.T)
        A = np.bmat([[2 * pts2, [[1],
                                 [1],
                                 [1]]],
                      [[[1, 1, 1, 0]]]])

        b = np.hstack((np.sum(pts * pts, axis=1), [1]))
        x = np.linalg.solve(A, b)
        bary_coords = x[:-1]
        center = np.dot(bary_coords, pts)
        radius = np.sum(np.square(pts[0] - center))
        return (center, radius)

    def in_circle(self, tri, p):
        center, radius = self.circles[tri]
        return np.sum(np.square(center - p)) <= radius

    def combine_polis(self, p):
        p = np.asarray(p)
        idx = len(self.coords)
        self.coords.append(p)

        divided = []
        for T in self.triangles:
            if self.in_circle(T, p):
                divided.append(T)
        boundary = []
        T = divided[0]
        edge = 0
        while True:
            tri_op = self.triangles[T][edge]
            if tri_op not in divided:
                boundary.append((T[(edge+1) % 3], T[(edge-1) % 3], tri_op))
                edge = (edge + 1) % 3
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                edge = (self.triangles[tri_op].index(T) + 1) % 3
                T = tri_op

        for T in divided:
            del self.triangles[T]
            del self.circles[T]
        new_triangles = []
        for (e0, e1, tri_op) in boundary:
            T = (idx, e0, e1)
            self.circles[T] = self.circumcenter(T)
            self.triangles[T] = [tri_op, None, None]
            if tri_op:
                for i, neigh in enumerate(self.triangles[tri_op]):
                    if neigh:
                        if e1 in neigh and e0 in neigh:
                            self.triangles[tri_op][i] = T

            new_triangles.append(T)
        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangles[T][1] = new_triangles[(i+1) % N]   # наступний
            self.triangles[T][2] = new_triangles[(i-1) % N]   # попередній

    def tris(self):
        return [(a-4, b-4, c-4) for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]


class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.y == other.y:
            return self.x > other.x
        return False

    def __repr__(self):
        return "Point: [x={},y={}]".format(self.x, self.y)


class Edge:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def cross(self, other):
        b = np.hstack((np.sum(self * other.T, axis=1), [1]))
        x = np.linalg.solve(self.p1, other.p1)
        return np.sum(np.square(b - x)) <= self.p1

class Triangle:

    def __init__(self, edges):
        self.edges = edges

groups = []

def divide_et_impera(points):
    """розділяй і володарюй"""
    num = len(points)
    print(points)
    if num == 3:
        print(points)
        groups.append([points])
    elif num == 4:
        #groups.append(points[:3])
        #groups.append(points[1:])
        groups.append([points[:3], points[1:]])
    elif num == 8:
        divide_et_impera(points[:4])
        divide_et_impera(points[4:])
        #map(divide_et_impera, [points[:4], points[4:]])
    elif num < 12:

        divide_et_impera(points[:3])
        divide_et_impera(points[3:])
        # map(divide_et_impera, [points[:3], points[3:]])
    else:
        half = int(num/2)
        center = np.mean(points, axis=0)
        divide_et_impera([p for p in points if p[0] >= center[0]])
        divide_et_impera([p for p in points if p[0] < center[0]])
        #print(points[:half])
        #map(divide_et_impera, [points[:half], points[half:]])


def circumcenter(pts):
    """
    Описане коло навколо трикутника (див скворцова пункт 1.3.1)
    """
    pts = np.array(pts)
    pts2 = np.dot(pts, pts.T)
    print(pts2)
    A = np.bmat([[2 * pts2, [[1],
                                [1],
                                [1]]],
                    [[[1, 1, 1, 0]]]])

    b = np.hstack((np.sum(pts * pts, axis=1), [1]))
    x = np.linalg.solve(A, b)
    bary_coords = x[:-1]
    center = np.dot(bary_coords, pts)
    radius = np.sum(np.square(pts[0] - center))
    return (center, radius)
    
def flip(tri1, tri2):
    tri1

def combine(group1, group2):
    pass

distribution = chaospy.J(chaospy.Uniform(0, 20), chaospy.Uniform(0, 20))
samples = distribution.sample(17, rule="hammersley")
points = samples.T
divide_et_impera(points)
print("gr = " + str(groups))
first = plt.figure(1)
fig, ax = plt.subplots()
for group in groups:
    for triangle in group:
        print(len(triangle))
        #print('group = ' + str(list(group[0])))
        cx, cy = zip(*triangle)
        plt.plot(cx, cy, marker="o", linestyle="")
        print('ssssss')
        print(circumcenter(triangle))
        center, radius = circumcenter(triangle)
        ax.add_artist(plt.Circle(center, radius**(1/2), color='k', fill=False, ls='dotted'))
        plt.fill(*zip(*triangle), fill=False, color="b", linestyle='-')
first.show()

dt = Delaunay(center, 22)
fig, ax = plt.subplots()
for s in points:
    dt.combine_polis(s) 
for group in groups:
    for triangle in group:
        cx, cy = zip(*triangle)
        plt.plot(cx, cy, marker="o", linestyle="")
cx, cy = zip(*points)
dt_tris = dt.tris()
ax.triplot(trian.Triangulation(cx, cy, dt_tris), 'b-')
plt.show()