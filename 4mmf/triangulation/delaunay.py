import numpy as np
from math import sqrt


class Delaunay:


    def __init__(self, center=(0, 0), radius=9999):
        """ Init and create a new frame to contain the triangulation
        center -- Optional position for the center of the frame. Default (0,0)
        radius -- Optional distance from corners to the center.
        """
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
        """
        Описане коло навколо трикутника (див скворцова пункт 1.3.1)
        """
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
        """Перевірка чи потрапляє точка в коло, описане навколо трикутника
        """
        center, radius = self.circles[tri]
        return np.sum(np.square(center - p)) <= radius

    def add_point(self, p):
        """Додаємо точку до поточної триангуляції (див Вступ глави 2 і пункт 2.1.1)
        """
        # Додаємо точку в масив вершин полігона
        p = np.asarray(p)
        idx = len(self.coords)
        self.coords.append(p)

        # Шукаємо трикутники, в коло яких потрапляє точка
        bad_triangles = []
        for T in self.triangles:
            if self.in_circle(T, p):
                bad_triangles.append(T)
        # Знайдемо межу (проти годинникової стрілки - ПГС) "поганих трикутників" у вигляді 
        # списку граней та протилежного трикутника для кожної грані
        boundary = []
        T = bad_triangles[0]
        edge = 0
        # пошук протилежного до грані трикутника
        while True:
            # Перевіряємо чи трикутник Т на межі
            tri_op = self.triangles[T][edge]
            if tri_op not in bad_triangles:
                # Додаємо до списку межі грань та протилежний трикутник
                boundary.append((T[(edge+1) % 3], T[(edge-1) % 3], tri_op))

                # Переходимо до наступної грані
                edge = (edge + 1) % 3

                # Перевіряємо чи межа замкнулася (умова виходу з циклу)
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                # Переходимо до наступної грані протилежного трикутника (ПГС)
                edge = (self.triangles[tri_op].index(T) + 1) % 3
                T = tri_op

        # Видаляємо непідходящі трикутники з поточного набору трикутників
        for T in bad_triangles:
            del self.triangles[T]
            del self.circles[T]

        # Робимо нову триангуляцію в "прогалині", яка залишилася після видалення трикутників
        new_triangles = []
        for (e0, e1, tri_op) in boundary:
            # Додаємо новий трикутник
            T = (idx, e0, e1)
            # Описуємо коло
            self.circles[T] = self.circumcenter(T)
            # Ставимо сусідній до Т трикутник як протилежний до щойно створеного
            self.triangles[T] = [tri_op, None, None]

            # І навпаки
            # Шукаємо сісдній трикутник до протилежного на  межі (e1, e0)
            if tri_op:
                for i, neigh in enumerate(self.triangles[tri_op]):
                    if neigh:
                        if e1 in neigh and e0 in neigh:
                            self.triangles[tri_op][i] = T

            new_triangles.append(T)

        # Додаємо вказівники нового і попереднього трикутників
        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangles[T][1] = new_triangles[(i+1) % N]   # наступний
            self.triangles[T][2] = new_triangles[(i-1) % N]   # попередній

    def export_triangles(self):
        """Список трикутників для виводу
        """
        return [(a-4, b-4, c-4)
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]

    def export_circles(self):
        """Список кіл для виводу
        """
        return [(self.circles[(a, b, c)][0], sqrt(self.circles[(a, b, c)][1]))
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]

