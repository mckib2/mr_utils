# NOT WORKING


import numpy as np
from mr_utils import view
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

if __name__ == '__main__':

    from mr_utils.test_data.phantom import binary_smiley
    from mr_utils.sim.traj import cartesian_pe

    N = 100
    m = binary_smiley(N)
    k = np.sum(np.abs(np.diff(m)) > 0)
    np.random.seed(5)
    samp = cartesian_pe(m.shape,undersample=.8,reflines=5)

    y = np.fft.fftshift(np.fft.fft2(m))*samp
    view(y,log=True)

    # m_hat = y.copy()
    m_hat = np.zeros(m.shape)
    alpha = 1
    lam = .1

    maxiter = 20
    for ii in range(maxiter):

        # Compute residual
        r = np.fft.fftshift(np.fft.fft2(m_hat)) - y

        # Fidelity term
        fidelity = np.abs(np.fft.ifft2(r))

        # Compute second term
        mu = np.finfo(float).eps
        m_hat = m_hat.flatten()
        first_term = m_hat[0]
        fd = np.diff(m_hat)
        m_hat = m_hat.reshape(m.shape)
        M = np.diag(np.reciprocal(np.abs(fd) + mu))
        second_term = np.hstack((first_term,np.dot(M,fd))).cumsum().reshape(m.shape)

        # Take the step
        m_hat -= alpha*(fidelity + lam*second_term)

        # view(m_hat)

        print(ii,compare_mse(m_hat/np.linalg.norm(m_hat),m/np.linalg.norm(m)))



    view(m_hat)
