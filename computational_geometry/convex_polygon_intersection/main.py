from intersection import *
import matplotlib.pyplot as plt

P = Polygon([Point(2,2), Point(2,-2), Point(-2,-2), Point(-2,2)])
Q = Polygon([Point(0,3), Point(3, 0), Point(0,-3)])
I = intersection(P, Q)


plt.figure(figsize=(8, 8))
plt.axis('equal')
plt.fill(P.x_s, P.y_s, facecolor='none', edgecolor='violet')
plt.fill(Q.y_s, Q.x_s, facecolor='none', edgecolor='purple')
plt.fill(I.y_s, I.x_s, facecolor='pink', edgecolor='red')
plt.show()