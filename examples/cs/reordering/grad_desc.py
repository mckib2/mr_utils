import numpy as np
from mr_utils import view
import matplotlib.pyplot as plt
from skimage.measure import compare_mse
from mr_utils.utils import dTV

if __name__ == '__main__':

    from mr_utils.test_data.phantom import binary_smiley
    from mr_utils.sim.traj import cartesian_pe

    N = 100
    m = binary_smiley(N)
    k = np.sum(np.abs(np.diff(m)) > 0)
    np.random.seed(5)
    samp = cartesian_pe(m.shape,undersample=.7,reflines=5)

    # Make the complex measurement in kspace
    y = np.fft.fftshift(np.fft.fft2(m))*samp

    m_hat = np.zeros(m.shape,dtype=y.dtype)
    alpha = .5
    lam = .01

    maxiter = 30
    for ii in range(maxiter):

        # Compute residual
        r = np.fft.fft2(m_hat)*samp - y

        # Fidelity term
        fidelity = np.fft.ifft2(r)

        # Sparsity term
        second_term = dTV(m_hat)

        # Take the step
        m_hat -= alpha*(fidelity + lam*second_term)

        print(ii,compare_mse(np.abs(m_hat),np.abs(m)))

    # Look at results
    view(m_hat)
