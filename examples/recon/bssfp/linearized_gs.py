'''Try another linearized geometric solution.'''

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils import view

if __name__ == '__main__':

    N = 256
    radius = 1
    T1 = 1.2
    T2 = .03
    M0 = 1
    TR = 10e-3
    alpha = np.deg2rad(30)
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    PD, T1, T2 = cylinder_2d(dims=(N, N), radius=radius)
    df = 100
    min_df, max_df = -df, df
    fx = np.linspace(min_df, max_df, N)
    fy = np.zeros(N)
    df, _ = np.meshgrid(fx, fy)

    I = ssfp(T1, T2, TR, alpha, df, pcs, PD, phi_rf=0)
    I_gs = gs_recon(I, second_pass=False)
    I_lgs = gs_recon(I)

    # 2*I_gs - (I2 + I3) = w0*(I0 - I2) + w1*(I1 - I3)
    A = np.stack((
        (I[0, ...] - I[2, ...]).flatten(),
        (I[1, ...] - I[3, ...]).flatten())).T
    b = (2*I_lgs - (I[2, ...] + I[3, ...])).flatten()
    w = np.linalg.lstsq(A, b, rcond=False)[0]
    I_lin = (
        w[0]*(I[0, ...] - I[2, ...]) + w[1]*(
            I[1, ...] - I[3, ...]) + (I[2, ...] + I[3, ...]))/2

    view(np.stack((I_gs, I_lgs, I_lin)))
