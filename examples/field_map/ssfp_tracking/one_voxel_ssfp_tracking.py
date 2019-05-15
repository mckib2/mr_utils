'''Find the nulls and lock on using dynamic RF pulse design.'''

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp
from mr_utils import view

if __name__ == '__main__':

    # Make the field inhomogeneity that we want to find
    T1 = 1.2
    T2 = .03
    M0 = 100
    pcs = np.linspace(0, 2*np.pi, 100)
    TR = 6e-3
    df = np.linspace(
        -1/TR, 1/TR, 100, endpoint=False)[
            np.random.randint(0, 100)]

    # Low alpha gives interesting profile shape, but we want
    # high flip angle so we get concave shape that's easy to
    # optimize
    alpha = np.deg2rad(90)

    # Take a look
    I = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0,
        delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)
    # view(I)

    # PC is the thing we'll try to dynamically change
    f = lambda x0: np.abs(ssfp(
        T1, T2, TR, alpha, df, phase_cyc=x0, M0=M0))

    # Find the null to begin with
    pc0 = 0
    pc = minimize(f, pc0)
    print(pc)
    pcx = pc['x'][0]

    # Get the shifted profile
    I0 = ssfp(
        T1, T2, TR, alpha, df,
        phase_cyc=np.linspace(pcx, pcx + 2*np.pi, 100),
        M0=M0)
    plt.plot(np.abs(I))
    plt.plot(np.abs(I0))
    plt.show()

    # Now we want to track the null as efficiently as possible.
    # The spectral profile is symmetric, but we can use phase
    # to know which slope we are climbing.  At each time point
    # we just need to adjust for the phase we observed, hoping
    # that the the observed phase varys smoothly.
    nt = 100
    t = np.arange(nt)
    f0 = 1/100
    ob_prev = ssfp(T1, T2, TR, alpha, df, pcx, M0)
    for ii, tt in enumerate(t):

        # df changes
        df += np.cos(tt*2*np.pi*f0)

        # Make a new observation using previous pcx estimate
        ob = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcx, M0=M0)

        # The true pc update would look like this:
        pcx -= np.cos(tt*2*np.pi*f0)*TR*2*np.pi

        # But we need to estimate this from our observation.
        # Assume that we've got a good estimate of the spectral
        # profile for this voxel, then we can match the
        # observation to the profile


        I = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0)
        I0 = ssfp(
            T1, T2, TR, alpha, df,
            phase_cyc=np.linspace(pcx, pcx + 2*np.pi, 100),
            M0=M0)
        plt.plot(np.abs(I))
        plt.plot(np.abs(I0))
        plt.show()
