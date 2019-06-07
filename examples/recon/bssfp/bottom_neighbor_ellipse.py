'''Use neighboring ellipses to tell us about the off-resonance.

Notes
-----
Estimate gradient of off-resonance, then do inverse gradient to get
back the actual off-resonance by assuming that off-resonance=0 at
isocenter.
'''

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils import view # pylint: disable=W0611

if __name__ == '__main__':

    N = 64
    radius = .9
    PD, T1, T2 = cylinder_2d((N, N), radius=radius)
    TR = 3e-3
    alpha = np.deg2rad(70)
    npcs = 4
    assert np.mod(npcs, 4) == 0
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)

    # Linear gradient off-resonance
    _, df = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N),
        np.linspace(-1/TR, 1/TR, N))

    # Try single coil
    I = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=0)
    # view(I)

    # Do lGS
    lGS = gs_recon(I, pc_axis=0)
    mask = np.abs(lGS) > .5
    # view(mask)
    # view(lGS)

    # Do for each pixel
    ddf_est = np.zeros((N-1, N))
    # ddf_true = np.zeros((N-1, N))
    for idx in np.ndindex((N-1, N)):
        ii, jj = idx[:]

        # Compare bottom neighbor
        xx0, yy0 = ii+1, jj
        xx1, yy1 = ii, jj

        if mask[xx0, yy0] and mask[xx1, yy1]:

            px0 = I[:, xx0, yy0]
            px1 = I[:, xx1, yy1]

            # First register the ellipse, i.e., rotate them to align.
            # They do not line up, but least squares fit should do
            # what we want
            px0_ctr = px0 - np.mean(px0.real) - 1j*np.mean(px0.imag)
            px1_ctr = px1 - np.mean(px1.real) - 1j*np.mean(px1.imag)
            ddf_est0 = np.linalg.lstsq(
                px0_ctr[:, None], px1_ctr, rcond=None)[0][0]
            ddf_est[ii, jj] = -1*np.angle(ddf_est0)

            import matplotlib.pyplot as plt
            from mr_utils.utils import fit_ellipse_halir, plot_conic
            px0_ctr = px0_ctr*np.exp(-1j*ddf_est[xx0, yy0])

            # Halir expects the points to be in the right order
            xs = np.zeros(npcs*2)
            ys = np.zeros(npcs*2)
            xs[1::2] = px0_ctr.real
            xs[::2] = px1_ctr.real
            ys[1::2] = px0_ctr.imag
            ys[::2] = px1_ctr.imag

            C = fit_ellipse_halir(xs, ys)
            x, y = plot_conic(C)
            plt.plot(x, y)
            plt.plot(px0_ctr.real, px0_ctr.imag)
            plt.plot(px1_ctr.real, px1_ctr.imag)
            plt.axis('square')
            plt.show()

    ddf_true = np.diff(df*np.pi*TR, axis=0)
    # view(np.stack((ddf_est, ddf_true)))

    ctr = int(N/2)
    df_true = ddf_true.cumsum(0)
    df_true -= df_true[ctr, ctr]

    df_est = ddf_est.cumsum(0)*mask[1:, :]
    df_est -= df_est[ctr, ctr]

    view(np.stack((df_true, df_est, df_true - df_est)))

    # view(df_est)
    # view(df[:, 0])
