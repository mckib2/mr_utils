import numpy as np
import matplotlib.pyplot as plt

def minmod(a,b):
    '''Flux limiter to make FD solutions total variation diminishing.'''
    val = ((np.sign(a) + np.sign(b))/2)*np.min((np.abs(a),np.abs(b)))
    return(val)

def check_stability(dt,h,c=3e8):
    '''Check stepsize restriction, imposed for for stability.'''
    return(dt/(h**2) <= c)

def getbounds(ii,jj,u0):
    # Consider boundary conditions
    xhigh = (ii + 1) == u0.shape[0]
    xlow = (ii - 1) == -1
    yhigh = (jj + 1) == u0.shape[1]
    ylow = (jj - 1) == -1

    if xhigh:
        xxhigh = ii
    else:
        xxhigh = ii + 1
    if xlow:
        xxlow = ii
    else:
        xxlow = ii - 1
    if yhigh:
        yyhigh = jj
    else:
        yyhigh = jj + 1
    if ylow:
        yylow = jj
    else:
        yylow = jj - 1

    return(xxhigh,xxlow,yyhigh,yylow)

def update_all_for_loop(u0,dt,h,sigma,niters):

    assert check_stability(dt,h),'Step size is unstable!'

    u = np.zeros((u0.shape[0],u0.shape[1],niters))
    u[:,:,0] = u0
    for nn in range(niters):
        for ii in range(u0.shape[0]):
            for jj in range(u0.shape[1]):

                # Get indices that account for boundary conditions
                xxhigh,xxlow,yyhigh,yylow = getbounds(ii,jj,u0)

                # Total Variation terms from dx,dy
                dxterm0 = (u[xxhigh,jj,nn] - u[ii,jj,nn])/np.sqrt( (u[xxhigh,jj,nn] - u[ii,jj,nn])**2 + (minmod( (u[ii,yyhigh,nn] - u[ii,jj,nn]),(u[ii,jj,nn] - u[ii,yylow,nn]) ))**2 )
                dxterm1 = (u[ii,jj,nn] - u[xxlow,jj,nn])/np.sqrt( (u[ii,jj,nn] - u[xxlow,jj,nn])**2 + (minmod( (u[xxlow,yyhigh,nn] - u[xxlow,jj,nn]),(u[xxlow,jj,nn] - u[xxlow,yylow,nn]) ))**2 )
                dxterm = dxterm0 - dxterm1

                dyterm0 = (u[ii,yyhigh,nn] - u[ii,jj,nn])/np.sqrt( (u[ii,yyhigh,nn] - u[ii,jj,nn])**2 + (minmod( (u[xxhigh,jj,nn] - u[ii,jj,nn]),(u[xxlow,jj,nn] - u[ii,jj,nn]) ))**2 )
                dyterm1 = (u[ii,jj,nn] - u[ii,yylow,nn])/np.sqrt( (u[ii,jj,nn] - u[ii,yylow,nn])**2 + (minmod( (u[xxhigh,yylow,nn] - u[ii,yylow,nn]),(u[xxlow,yylow,nn] - u[ii,yylow,nn]) ))**2 )
                dyterm = dyterm0 - dyterm1

                # Fidelity term from u - u0
                lambdacumsum = 0
                for ii0 in range(u0.shape[0]):
                    for jj0 in range(u0.shape[1]):
                        xxhigh0,xxlow0,yyhigh0,yylow0 = getbounds(ii0,jj0,u0)

                        lambdaterm0 = np.sqrt( (u[xxhigh0,jj0,nn] - u[ii0,jj0,nn])**2 + (u[ii0,yyhigh0,nn] - u[ii0,jj0,nn])**2 )
                        lambdaterm1 = (u[xxhigh0,jj0,0] - u[ii0,jj0,0])*(u[xxhigh0,jj0,nn] - u[ii0,jj0,nn])
                        lambdaterm2 = (u[ii0,yyhigh0,0] - u[ii0,jj0,0])*(u[ii0,yyhigh0,nn] - u[ii0,jj0,nn])
                        lambdacumsum += lambdaterm0 - lambdaterm1/lambdaterm0 - lambdaterm2/lambdaterm0

                lambdaterm = (-h/(2*sigma**2))*lambdacumsum

                # Update next time step using all the update terms
                u[ii,jj,nn+1] = u[ii,jj,nn] + (dt/h)*(dxterm + dyterm) - dt*lambdaterm*(u[ii,jj,nn] - u[ii,jj,0])

    print(u)
    return(u)

if __name__ == '__main__':
    pass
