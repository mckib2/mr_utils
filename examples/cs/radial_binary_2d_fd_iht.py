import numpy as np
import matplotlib.pyplot as plt
from mr_utils.sim.traj import radial
# from mr_utils.cs import IHT,cosamp
from mr_utils.utils.printtable import Table
from mr_utils.test_data.phantom import binary_smiley

if __name__ == '__main__':

    # We want a 2d signal, so let's make a binary smiley face
    N = 50
    smiley = binary_smiley(N)

    # Make sure it looks alright
    plt.imshow(smiley)
    plt.title('Phantom')
    plt.show()

    # True signal
    m = smiley.flatten()

    # Create undersampling pattern, try golden angle
    num_spokes = 72
    samp = radial(smiley.shape,num_spokes,skinny=True,extend=False)
    plt.imshow(samp)
    plt.title('Sampling pattern, %d rays' % num_spokes)
    plt.show()

    # Construct undersampled fourier transform matrix
    A = np.fft.fftshift(np.fft.fft(np.eye(N,N)))
    E = np.diag(samp.flatten()).dot(np.kron(A,A))
    E /= np.sqrt(np.sum(np.abs(E)**2,axis=0))
    s = E.dot(m.conj())

    # Look at how incoherent the sampling matrix is (we want it to be eye)
    plt.imshow(np.abs(E.conj().T.dot(E)))
    plt.title('Matrix incoherency (want it look like identitiy matrix)')
    plt.show()
    # Actually doesn't look too bad...

    # Do the IHT, modified to include sampling model
    maxiter = 50 # dimishing returns after this
    disp = True
    tol = 1e-8
    k = np.sum(np.abs(np.diff(m)) > 0)
    samples = np.sum(samp,axis=(0,1))
    print('k: %d, num_samples: %d' % (k,samples))
    mu = .8

    # Run until tol reached or maxiter reached
    table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
    print(table.header())
    m_hat = np.zeros(s.size,dtype=s.dtype)
    r = s.copy()
    for tt in range(int(maxiter)):

        # We'll loose the first sample to the diff operator
        first_m = m_hat[0]

        # Transform into finite differences domain
        fd = np.diff(E.conj().T.dot(r))

        # Hard thresholding
        fd[np.argsort(np.abs(fd))[:-k]] = 0

        # Inverse transform and take the step
        m_hat += mu*np.hstack((first_m,fd)).cumsum()

        # This may or may not be a good stopping criteria for this
        stop_criteria = np.linalg.norm(r)/np.linalg.norm(s)

        # Show MSE at current iteration if we wanted it
        if disp:
            print(table.row([ tt,stop_criteria,np.mean((np.abs(m - m_hat)**2)) ]))

        # Check stopping criteria
        if stop_criteria < tol:
            break

        # Get new residual
        r = s - E.dot(m_hat)


    plt.imshow(np.abs(m_hat.reshape(smiley.shape)))
    plt.title('IHT Recon')
    plt.show()
