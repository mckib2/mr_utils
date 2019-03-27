'''Example showing how phase-cycles lie on spectral profile.

Currently either I'm doing something wrong or there needs to be some
phase correction to match the actual spectral profile.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp, elliptical_params

if __name__ == '__main__':

    # SSFP experiment params
    TR = 10e-3
    alpha = np.deg2rad(10)
    lpcs = 64
    pcs = np.linspace(-2*np.pi, 2*np.pi, lpcs, endpoint=False)

    # Experiment conditions and tissue params
    T1 = .750
    T2 = .035
    M0 = 1
    df = 0
    dfs = np.linspace(-1/TR, 1/TR, lpcs, endpoint=False) + df

    # Do the thing once with no phi_rf, once with to see difference
    I = ssfp(T1, T2, TR, alpha, df, pcs, M0, phi_rf=0)
    Idf = ssfp(T1, T2, TR, alpha, dfs, pcs[0], M0, phi_rf=0)

    pcs_deg = np.rad2deg(pcs)
    aI = np.angle(I)
    aIdf = np.angle(Idf)


    # # It appears that we need to do a phase correction!
    # M, a, b = elliptical_params(T1, T2, TR, alpha, M0)
    # thetan = 2*np.pi*dfs*TR
    # phin = np.pi*dfs*TR
    # num0 = a*np.sin(thetan + phin) - np.sin(phin)
    # den0 = a*np.cos(thetan + phin) - np.cos(thetan)
    #
    # thetam = pcs
    # phim = 0
    # num1 = a*np.sin(thetam + phim) - np.sin(phim)
    # den1 = a*np.cos(thetam + phim) - np.cos(thetam)
    #
    # num = np.arctan2(num0, den0)
    # den = np.arctan2(num1, den1)
    # fac = 1/(num/den)
    #
    # plt.plot(aI/aIdf)
    # plt.plot(fac)
    # plt.plot(np.sqrt(np.abs(aI - pcs)))
    # # plt.plot(np.abs(aIdf))
    # plt.show()
    #
    # # aI = np.sqrt(np.abs(aI - 5*pcs/6))*np.sign(aI - pcs)
    # aI /= fac

    # Look at the spectral profile
    fig, ax1 = plt.subplots()
    ax1.plot(pcs_deg, np.abs(I))
    ax1.plot(pcs_deg, np.abs(Idf), '--')
    ax1.set_ylabel('Magnitude')
    ax1.set_xlabel('Phase-cycle (deg)')

    ax2 = ax1.twinx()
    ax2.plot(pcs_deg, aI, '--', label='Phase, pcs')
    ax2.plot(pcs_deg, aIdf, '--', label='Phase, dfs')
    ax2.set_ylabel('Phase (rad)')
    ax2.set_xlabel('Phase-cycle (deg)')
    ax2.legend()

    plt.show()
