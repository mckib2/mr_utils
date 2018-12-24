import numpy as np

def linesearch_quad(f,x,a,s):
    f1 = f(x + a*s)
    f2 = f(x + 2*a*s)
    f3 = f(x + 4*a*s)
    a *= (-f1*12 + f2*15 - f3*2)/(2*(-f1*2 + f2*3 - f3))
    return(a)

def linesearch(obj,x0,a0,s):
    f = [ obj(x0),obj(x0 + a0*s) ] # initial conditions
    a = [ 0,a0 ]
    t = 1.3 # factor of increase

    n = len(x0);

    while (f[-1] < f[-2]) | (len(np.unique(f)) < n):
        a.append(a[-1]*t)
        f.append(obj(x0 + a[-1]*s))

    # Go back and fill in
    a_new = a[0::-1]
    a_new.append((a[-1] + a[-2])/2)
    a_new.append(a[-1])
    a = np.array(a_new)

    f_new = f[0::-1]
    f_new.append(obj(x0 + a[-2]*s))
    f_new.append(f[-1])
    f = f_new

    # Get rid of duplicate values if we have any
    f,idx = np.unique(f,return_index=True)
    a = a[idx]

    # I see people switching between quadratic and cubic fits, but we'll
    # just assume a quadratic for ease
    a = (f[0]*(a[1]**2 - a[2]**2) + f[1]*(a[2]**2 - a[0]**2) + f[2]*(a[0]**2 - a[1]**2))/(2*(f[0]*(a[1] - a[2]) + f[1]*(a[2] - a[0]) + f[2]*(a[0] - a[1])))
    return(a)
