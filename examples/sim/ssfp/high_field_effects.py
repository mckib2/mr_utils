'''If field map is large, strange things happen.

Notes
-----
If the field is strong, the banding frequency is increased.  If the
resolution is too low, multiple bands will be contained in a single
voxel leading to bad artifacts in the GS recon or other SSFP models.
'''

import numpy as np

from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

if __name__ == '__main__':

    # Get a 2D image, since we can't seem to replicate using a single
    # voxel
    N = 64
    df_noise_std = 0
    radius = .8
    TR = 6e-3
    alpha = np.deg2rad(30)
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    PD, T1, T2 = cylinder_2d(dims=(N, N), radius=radius)

    df = 1000
    min_df, max_df = -df, df
    fx = np.linspace(min_df, max_df, N)
    fy = np.zeros(N)
    df, _ = np.meshgrid(fx, fy)

    if df_noise_std > 0:
        n = np.random.normal(0, df_noise_std, df.shape)
        df += n

    I = ssfp(T1, T2, TR, alpha, df, pcs, PD, phi_rf=0)


    recon = gs_recon(I, pc_axis=0)
    print(I.shape)

    I0 = np.concatenate((I, recon[None, ...]), axis=0)
    view(I0, montage_axis=0)
