import numpy as np
import matplotlib.pyplot as plt

def minmod(a,b):
    '''Flux limiter to make FD solutions total variation diminishing.'''
    val = ((np.sign(a) + np.sign(b))/2)*np.min((np.abs(a),np.abs(b)))
    return(val)

def check_stability(dt,h,c=3e8):
    '''Check stepsize restriction, imposed for for stability.'''
    return(dt/(h**2) <= c)

def update_all_for_loop(u0,dt,h,sigma,niters):

    assert check_stability(dt,h),'Step size is unstable!'

    u = np.zeros((u0.shape[0],u0.shape[1],niters))
    u[:,:,0] = u0
    for nn in range(1,niters):
        for ii in range(1,u0.shape[0]):
            for jj in range(1,u0.shape[1]):

                # Total Variation terms from dx,dy
                dxterm0 = (u[ii+1,jj,nn] - u[ii,jj,nn])/np.sqrt( (u[ii+1,jj,nn] - u[ii,jj,nn])**2 + (minmod( (u[ii,jj+1,nn] - u[ii,jj,nn]),(u[ii,jj,nn] - u[ii,jj-1,nn]) ))**2 )
                dxterm1 = (u[ii,jj,nn] - u[ii-1,jj,nn])/np.sqrt( (u[ii,jj,nn] - u[ii-1,jj,nn])**2 + (minmod( (u[ii-1,jj+1,nn] - u[ii-1,jj,nn]),(u[ii-1,jj,nn] - u[ii-1,jj-1,nn]) ))**2 )
                dxterm = dxterm0 - dxterm1

                dyterm0 = (u[ii,jj+1,nn] - u[ii,jj,nn])/np.sqrt( (u[ii,jj+1,nn] - u[ii,jj,nn])**2 + (minmod( (u[ii+1,jj,nn] - u[ii,jj,nn]),(u[ii-1,jj,nn] - u[ii,jj,nn]) ))**2 )
                dyterm1 = (u[ii,jj,nn] - u[ii,jj-1,nn])/np.sqrt( (u[ii,jj,nn] - u[ii,jj-1,nn])**2 + (minmod( (u[ii+1,jj-1,nn] - u[ii,jj-1,nn]),(u[ii-1,jj-1,nn] - u[ii,jj-1,nn]) ))**2 )
                dyterm = dyterm0 - dyterm1

                # Fidelity term from u - u0
                # TODO: This is supposed to sum over all ii,jj
                lambdaterm0 = np.sqrt( (u[ii+1,jj,nn] - u[ii,jj,nn])**2 + (u[ii,jj+1,nn] - u[ii,jj,nn])**2 )
                lambdaterm1 = (u[ii+1,jj,0] - u[ii,jj,0])*(u[ii+1,jj,nn] - u[ii,jj,nn])
                lambdaterm2 = (u[ii,jj+1,0] - u[ii,jj,0])*(u[ii,jj+1,nn] - u[ii,jj,nn])
                lambdaterm = (-h/(2*sigma**2))*np.sum(lambdaterm0 - lambdaterm1/lambdaterm0 - lambdaterm2/lambdaterm0,axis=(0,1))
                # lambdaterm = 0

                # Update next time step using all the update terms
                u[ii,jj,nn+1] = u[ii,jj,nn] + (dt/h)*(dxterm + dyterm) - dt*lambdaterm*(u[ii,jj,nn] - u[ii,jj,0])

    return(u)

if __name__ == '__main__':
    pass
