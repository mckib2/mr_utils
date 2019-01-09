import numpy as np
import matplotlib.pyplot as plt

def IT(eta,y,shape,mu=1,x=0,tol=1e-8,maxiter=200):

    # Initial estimate of x is zero
    x_hat = np.zeros(shape)

    # Get initial residue
    r = y.copy()

    # Run until tol reached or maxiter reached
    prev_stop_criteria = np.inf
    for tt in range(int(maxiter)):

        # Take a step and threshold, all in one!
        x_hat = eta(x_hat=x_hat,r=r,mu=mu)

        stop_criteria = np.linalg.norm(r)/np.linalg.norm(y)

        # If the stop_criteria gets worse, get out of dodge
        if stop_criteria > prev_stop_criteria:
            break
        prev_stop_criteria = stop_criteria

        # # Show MSE at current iteration if we wanted it
        # if disp:
        print([ tt,stop_criteria,np.mean((np.abs(x - x_hat)**2)) ])

        # update the residual
        r = y - eta(x_hat=x_hat)

        # Check stopping criteria
        if stop_criteria < tol:
            break

    return(x_hat)

if __name__ == '__main__':

    from mr_utils.test_data.phantom import binary_smiley
    from mr_utils.sim.traj import cartesian

    N = 500
    x = binary_smiley(N)
    k = np.sum(np.abs(np.diff(x)) > 0)
    samp = cartesian(x.shape,undersample=.5,reflines=5)

    def eta(x_hat=None,r=None,mu=1):
        if x_hat is not None and r is None:
            kspace = np.fft.fftshift(np.fft.fft2(x_hat))
            kspace_u = kspace*samp
            return(kspace_u)
        else:

            # Density compensation!!!!
            #

            # Take step
            val = (x_hat + mu*np.abs(np.fft.ifft2(r))).flatten()

            # Finite differences transformation
            first_samp = val[0] # save the first sample for inverse transform
            fd = np.diff(val)

            # Hard thresholding
            fd[np.argsort(np.abs(fd))[:-k]] = 0

            # Inverse finite differences transformation
            res = np.hstack((first_samp,fd)).cumsum().reshape(x_hat.shape)
            return(res)

    # Simulate acquisiton
    y = eta(x_hat=x)

    # Do IHT, enforcing sparsity in finite differences domain
    x_hat = IT(eta,y,x.shape,mu=1,x=x,maxiter=100)

    # Check it out
    plt.imshow(np.abs(x_hat))
    plt.show()
