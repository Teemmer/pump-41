import math
import numpy as np

from single_var import Minimizer


def alpha_func(x, H):
    def func(alpha):
        return f(x - alpha * np.dot(H, np.array([nabla_f(x)]).T).T[0])
    return func

class MultiMinimizer:

    def __init__(self, eps, x0, max_iter=1000):
        self.eps = eps
        self.x0 = x0
        self.max_iter = max_iter

    def newton(self):
        k = 0
        x = [self.x0]
        while k <= self.max_iter:
            norm = max(map(abs, nabla_f(x[k])))
            if norm <= self.eps:
                return x[k]
            inverse = np.linalg.inv(der2_f(x[k]))
            print(inverse)
            alpha = Minimizer(
                func=alpha_func(x[k], inverse), 
                eps=self.eps,
                start_segment=[0,1]).fibonacci()        
            print('alpha=' + str(alpha))
            x.append(x[k] - alpha * np.dot(inverse, np.array([nabla_f(x[k])]).T).T[0])
            # x.append(x[k] - alpha * np.dot(inverse, nabla_f(x[k])))
            
            print(x[k+1])
            print('f(x) = ' + str(f(x[k])))
            if f(x[k+1]) > f(x[k]):     
                print("bigger, something wrong (probably there's no global minimum((()")
                return 0
            if abs(f(x[k+1]) - f(x[k])) < self.eps:
                return x[k+1]
            print(k)
            k += 1

    def broyden(self):
        k = 0
        H = np.eye(len(self.x0))
        x = [self.x0]
        while k <= self.max_iter:
            # alpha = 1
            # x_new = x[k] - alpha * np.dot(H, np.array([nabla_f(x[k])]).T).T[0]
            # while f(x[k]) * alpha > f(x_new):
            #     alpha = alpha / 2
            #     x_new = x[k] - alpha * np.dot(H, np.array([nabla_f(x[k])]).T).T[0]
            # x.append(x_new)
            minim = Minimizer(
                func=alpha_func(x[k], H), 
                eps=self.eps,
                start_segment=[0,1])
            alpha = minim.fibonacci()
            print('alpha=' + str(alpha))
            x.append(x[k] - alpha * np.dot(H, np.array([nabla_f(x[k])]).T).T[0])
            print('x= ' + str(x[k+1]))
            print('f(x) = ' + str(f(x[k])))
            print(k)
            if f(x[k+1]) > f(x[k]):
                print("bigger, something wrong (probably there's no global minimum((()")
                return 0
            if np.isnan(x[k+1][0]):
                return "NAN"
            if max(map(abs, x[k+1] - x[k])) < self.eps:
                return x[k+1]
            d_y = nabla_f(x[k+1]) - nabla_f(x[k])
            d_x = x[k+1] - x[k]
            if k == 0 or max(map(abs, H[0] - H_new[0])) > self.eps:
                x_minus_Hy = np.array([d_x - np.dot(H, np.array([d_y]).T).T[0]])
                H_new = H + np.dot(x_minus_Hy.T, x_minus_Hy) / np.dot(x_minus_Hy, d_y)[0]
                H_new, H = H, H_new
            k += 1

def nabla_f(x):
    # sin = math.sin(0.5*(x[0]-x[1]))
    # return np.array([4*x[0]+sin, 6*x[1]+1-sin])
    # e = math.exp(x[0]**2 + x[1]**2)
    # return np.array([(2*x[0]*e) + 1, (2*x[1]*e) + 5])
    # return np.array([4*x[0]+x[1], x[0]+2*x[1]])
    return np.array([x[1]+4*x[0],x[0]])
    return np.array([2 * x[0] * math.exp(x[0] **2 + x[1]**2) + 4 + 2 * x[0], 
    2 * x[1] * math.exp(x[0] **2 + x[1]**2) + 3])
    return np.array([
        x[0]/math.sqrt(x[0]**2 + x[1]**2 + 2) - 2 + 4*(x[0]**3),
        x[1]/math.sqrt(x[0]**2 + x[1]**2 + 2) + 3 + 4*(x[1]**3),
        ])

def der2_f(x):
    # cos = math.cos(0.5*(x[0]-x[1]))
    # return np.array([
    #     [4 + 0.5*cos, -0.5*cos],
    #     [-0.5*cos, 6 + 0.5*cos]
    # ])
    # e = math.exp(x[0]**2 + x[1]**2)
    # return np.array([
    #     [(2+4*(x[0]**2))*e, 4*x[0]*x[1]*e],
    #     [4*x[0]*x[1]*e, (2+4*(x[1]**2))*e]
    # ])
    # return np.array([[4,1],[1,2]])
    return [[2 * math.exp(x[0] **2 + x[1]**2) + 4 * x[0] * x[0] * math.exp(x[0] **2 + x[1]**2) + 2,
         4 * x[0] * x[1] * math.exp(x[0] **2 + x[1]**2)],
        [4 * x[0] * x[1] * math.exp(x[0] **2 + x[1]**2),
         2 * math.exp(x[0] **2 + x[1]**2) + 4 * x[1] * x[1] * math.exp(x[0] **2 + x[1]**2)]]
    brackets = x[0]**2 + x[1]**2 + 2
    return np.array([
        [brackets**(-1/2) - x[0]**2 * (-12 + brackets**(-3/2)), -x[0]*x[1]*(brackets**(-3/2))], 
        [-x[0]*x[1]*(brackets**(-3/2)), brackets**(-1/2) - x[1]**2 * (-12 + brackets**(-3/2))]
        ])

def f(x):
    # return 2*(x[0]**2) + 3*(x[1]**2) - 2*math.cos(0.5*(x[0]-x[1])) + x[1]
    # return math.exp(x[0]**2 + x[1]**2) + x[0] + 5*x[1]
    # return 2* (x[0] ** 2) + x[0]*x[1] + x[1]**2 
    return x[0]*x[1] + 2*(x[0]**2)
    return math.exp(x[0] * x[0]  + x[1]  * x[1] ) + 4 * x[0]  + 3 * x[1]  + x[0]*x[0]
    return math.sqrt(x[0]**2 + x[1]**2 + 2) - 2*x[0] + 3*x[1] + x[0]**4 + x[1]**4

if __name__ == "__main__":
    m_min = MultiMinimizer(
        eps=1e-2,
        x0=[1,1]
        )
    print(m_min.broyden())
    
