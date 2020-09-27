import math

class Minimizer:
    """
    text    
    """

    def __init__(self, func, der_func, step, eps, start_point):
        self.func = func
        self.der_func = der_func
        self.step = step
        self.eps = eps
        self.start_point = start_point
        self._get_start_local_segment()

    def _get_start_local_segment(self):
        """ get localized segment"""
        k = 0
        x = [self.start_point]
        h = [self.step]
        f_x = self.func(x[0])
        f_x_plus_h = self.func(x[0] + h[0])
        if f_x < f_x_plus_h:
            h[0] = -h[0]
            if f_x_plus_h <= f_x >= self.func(x[0] + h[0]):
                self.start_local_segment = None
            if self.func(x[0] + abs(h[0])) > f_x and \
                self.func(x[0] - abs(h[0])) > f_x and \
                abs(h[0]) < self.eps:
                self.start_local_segment = x[0]

        while self.func(x[k]) > self.func(x[k] + h[k]):
            h.append(2*h[k])
            x.append(x[k] + h[k])
            k += 1
        h.append(2*h[k])
        x.append(x[k] + h[k])
        x_m = x[-3:]
        x_m.insert(2, x_m[-1]-h[k]/2)
        f_m = list(map(self.func, x_m))
        x_m.pop(0) if f_m[0] > f_m[-1] else x_m.pop()
        self.start_local_segment = sorted([x_m[0], x_m[-1]])
        return self.start_local_segment

    def cut_segment_half(self):
        """minimum of function"""
        segment = [self.start_local_segment]
        k=0
        x=[]
        while abs(segment[k][0] - segment[k][1]) > self.eps:
            x.append((segment[k][0] + segment[k][1])/2)
            if self.der_func(x[k]) == 0:
                return x[k]
            elif self.der_func(x[k]) > 0:
                segment.append([segment[k][0], x[k]])
            else:
                segment.append([x[k], segment[k][1]])
            print(segment[k+1])
            k += 1
        return (segment[k][0] + segment[k][1])/2


    def fibonacci(self):
        """fibonacci minimization"""

        segment = [self.start_local_segment]
        print(self.start_local_segment)
        fib = fibonacci()
        fib_numbers = [1, next(fib), next(fib)]
        k = 0
        y = []
        z = []
        n = 2
        while True:
            i = next(fib)
            fib_numbers.append(i)
            n += 1
            if i >= (segment[0][1] - segment[0][0])/self.eps:
                break
        y.append(segment[k][0] + fib_numbers[-3]/fib_numbers[-1]*(segment[k][1] - segment[k][0]))
        z.append(segment[k][1] + segment[k][0] - y[k])
        while k != n - 3:
            print(k)
            print("y=" + str(y[k]) + "  z=" + str(z[k]))
            print("a=" + str(segment[k][0]) + "  b=" + str(segment[k][1]))
            if self.func(y[k]) <= self.func(z[k]):
                segment.append([segment[k][0], z[k]])
                z.append(y[k])
                y.append(segment[k+1][1] + segment[k+1][0] - z[k+1])
            else:
                segment.append([y[k], segment[k][1]])
                y.append(z[k])
                z.append(segment[k+1][1] + segment[k+1][0] - y[k+1])
            fib_numbers.pop()
            k += 1
        print("a=" + str(segment[k][0]) + "  b=" + str(segment[k][1]))
        return (segment[k][0] + segment[k][1])/2

    def dichotomy(self, sigma):
        """dichotomy minimization"""
        segment = [self.start_local_segment]
        k = 0
        y = []
        z = []
        while abs(segment[k][0] - segment[k][1]) > self.eps and k < 1000:
            y.append((segment[k][0] + segment[k][1] - sigma)/2)
            z.append((segment[k][0] + segment[k][1] + sigma)/2)
            if self.func(y[k]) <= self.func(z[k]):
                segment.append([segment[k][0], z[k]])
            else:
                segment.append([y[k], segment[k][1]])
            print(segment[k+1])
            k += 1
        return (segment[k][0] + segment[k][1])/2

    def golden_ratio(self):
        """golden ratio minimization"""
        segment = [self.start_local_segment]
        k = 0
        y = [segment[0][0] + (3 - math.sqrt(5))*(segment[0][1] - segment[0][0])/2]
        z = [segment[0][1] + segment[0][0] - y[0]]
        while abs(segment[k][0] - segment[k][1]) > self.eps:
            if self.func(y[k]) <= self.func(z[k]):
                segment.append([segment[k][0], z[k]])
                z.append(y[k])
                y.append(segment[k+1][0] + segment[k+1][1] - z[k+1])
            else:
                segment.append([y[k], segment[k][1]])
                y.append(z[k])
                z.append(segment[k+1][0] + segment[k+1][1] - y[k+1])
            k += 1
        return (segment[k][0] + segment[k][1])/2


def fibonacci():
    x_prev = 1
    x = 1
    while True:
        x_prev, x = x, x + x_prev
        yield x_prev


def der_func(x):
    #return (x-5)*2
    return 4*(x**3) + 2*x + 1
    #return 3*(x*2) + 6
    #return 2*(x**2)-12*x   


def func(x):
    #return (x-5)**2
    return x**4 + x**2 + x + 1
    #return 3*(x**2) + 6*x - 2
    #return 2*(x**2)-12*x 


if __name__ == '__main__':
    minimizer = Minimizer(
        func=func, 
        der_func=der_func,
        step=1, 
        eps=0.0002, 
        start_point=0
        )
    half = minimizer.cut_segment_half()
    fib = minimizer.fibonacci()
    dih = minimizer.dichotomy(0.0005)
    gold = minimizer.golden_ratio()
    print(func(half))
    print(func(fib))
    print(func(dih))
    print(func(gold))