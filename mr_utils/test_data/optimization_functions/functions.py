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

def ackley(x,a=20,b=0.2,c=2*np.pi):
    '''Ackley function.'''
    d = x.size
    return(-a*np.exp(-b*np.sqrt(np.sum(x**2)/d)) - np.exp(np.sum(np.cos(c*x))/d) + a + np.exp(1))
    # return(-a*np.exp(-b*np.sqrt(.5*(x[0]**2 + x[1]**2))) - np.exp(.5*(np.cos(c*x[0]) + np.cos(c*x[1]))) + np.exp(1) + a)

def grad_ackley(f,x,a=20,b=0.2,c=2*np.pi):
    '''Gradient of Ackley function.'''
    d = x.size
    return(a*b*x/(np.finfo(float).eps + np.sqrt(1/d*np.sum(x**2)))*np.exp(-b*np.sqrt(np.sum(x**2)/d)) - a*c/d*np.sin(c*x)*np.exp(-np.sum(np.cos(c*x))/d))
    
def sphere(x):
    '''Sphere function.'''
    return(np.sum(x**2))

def beale(x):
    '''Beale function.

    Only for 2d x.
    '''
    return((1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2)

def bohachevsky1(x):
    '''Bohachevsky function 1.
    Only for 2d x.
    '''
    return(x[0]**2 + 2*x[1]**2 - .3*np.cos(3*np.pi*x[0]) - .4*np.cos(4*np.pi*x[1]) + .7)

def grad_bohachevsky1(f,x):
    '''Gradient of Bohachevsky function 1.'''
    return(np.array([ 2*x[0] + .9*np.pi*np.sin(3*np.pi*x[0]), 4*x[1] + .16*np.pi*np.sin(4*np.pi*x[1]) ]))

def bohachevsky2(x):
    '''Bohachevsky function 2.
    Only for 2d x.
    '''
    return(x[0]**2 + 2*x[1]**2 - 0.3*np.cos(3*np.pi*x[0])*np.cos(4*np.pi*x[1]) + 0.3)

def grad_bohachevsky2(f,x):
    '''Gradient of Bohachevsky function 2.'''
    return(np.array([ 2*x[0] + .9*np.pi*np.cos(4*np.pi*x[1])*np.sin(3*np.pi*x[0]), 4*x[1] + .12*np.pi*np.cos(3*np.pi*x[0])*np.sin(4*np.pi*x[1]) ]))

def bohachevsky3(x):
    '''Bohachevsky function 3.
    Only for 2d x.
    '''
    return(x[0]**2 + 2*x[1]**2 - 0.3*np.cos(3*np.pi*x[0] + 4*np.pi*x[1]) + 0.3)

def grad_bohachevsky3(f,x):
    '''Gradient of Bohachevsky function 3.'''
    return(np.array([ 2*x[0] + .9*np.pi*np.sin(3*np.pi*x[0] + 4*np.pi*x[1]), 4*x[1] + .12*np.pi*np.sin(3*np.pi*x[0] + 4*np.pi*x[1]) ]))
