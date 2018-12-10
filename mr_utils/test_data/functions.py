'''Test functions for optimization.

See:
    https://en.wikipedia.org/wiki/Test_functions_for_optimization
'''

import numpy as np

def quadratic(x):
    return(x**4 - 3*x**3 + 2)

def rosenbrock(x,a=1,b=100):
    '''Rosenbrock's function.'''
    xp = x[1:]
    return(np.sum(b*(xp - x[:-1]**2)**2 + (a - x[:-1])**2 ))

def rastrigin(x,A=10):
    '''Rastrigin function.'''
    n = x.size
    return(A*n + np.sum(x**2 - A*np.cos(2*np.pi*x)))

def ackley(x):
    '''Ackley function.'''
    return(-20*np.exp(-.2*np.sqrt(.5*(x[0]**2 + x[1]**2))) - np.exp(.5*(np.cos(2*np.pi*x[0]) + np.cos(2*np.pi*x[1]))) + np.exp(1) + 20)

def sphere(x):
    '''Sphere function.'''
    return(np.sum(x**2))

def beale(x):
    '''Beale function.'''
    return((1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2)
