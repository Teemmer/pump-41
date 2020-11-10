import matplotlib.pyplot as plt
import matplotlib.tri
import numpy as np
import chaospy
from delaunay import Delaunay

if __name__ == '__main__':

    numSeeds = 11
    radius = 20
    a, b = 5, 4
    border = [[radius*0,radius*0], [radius*0,radius*b], [radius*a,radius*0], [radius*a, radius*b]]
    #seeds = (radius-1) * np.random.random((numSeeds, 2))
    distribution = chaospy.J(chaospy.Uniform(0, a), chaospy.Uniform(0, b))
    samples = distribution.sample(numSeeds, rule="hammersley")
    print(list(samples.T))
    border.extend(list(radius * samples.T))
    print(border)
    #seeds = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    seeds = border

    center = np.mean(seeds, axis=0)
    dt = Delaunay(center, (50 + a) * radius)

    for s in seeds:
        dt.add_point(s)



    fig, ax = plt.subplots()
    ax.margins(0.1)
    ax.set_aspect('equal')
    plt.axis([-1, radius * a + 1, -1, radius * b + 1])

    # Грані
    cx, cy = zip(*seeds)
    dt_tris = dt.export_triangles()
    ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')

    # Вершини

    for i, v in enumerate(seeds):
        plt.annotate(i, xy=v)
    # Кола

    for c, r in dt.export_circles():
        ax.add_artist(plt.Circle(c, r, color='k', fill=False, ls='dotted'))
    plt.show()

    # Покроковий вивід

    dt2 = Delaunay(center, 50 * radius)
    NT=[]
    for i,s in enumerate(seeds):
        print("Inserting seed", i, s)
        dt2.add_point(s)
        # if i > 1: # Показувати всі кроки
        if i == len(seeds) - 1:
            fig, ax = plt.subplots()
            ax.margins(0.1)
            ax.set_aspect('equal')
            plt.axis([-1, radius* a + 1, -1, radius * b + 1])
            for i, v in enumerate(seeds):
                plt.annotate(i, xy=v)            
            tri_num = 0
            for t in dt2.export_triangles():
                print(t)
                tri_num += 1
                polygon = [seeds[i] for i in t]    
                plt.text((polygon[0][0] + polygon[1][0] + polygon[2][0]) / 3,
                            (polygon[0][1] + polygon[1][1] + polygon[2][1]) / 3,tri_num.__str__(),
                         size=10, bbox=dict(boxstyle="square",
                                   ec=(1., 1., 1.),
                                   fc=(0.8, 0.8, 1.),))
                plt.fill(*zip(*polygon), fill=False, color="b") 
            plt.show()
