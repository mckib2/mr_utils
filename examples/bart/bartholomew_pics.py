'''"non-Cartesian MRI using BART"

Adapted from:
    https://mrirecon.github.io/bart/examples.html
'''

import numpy as np

from mr_utils.bart import Bartholomew as B
from mr_utils import view

if __name__ == '__main__':

    # Generate k-space trajectory with num_spokes radial spokes
    num_spokes = 32
    traj_rad = B.traj(x=512, y=num_spokes, r=True)

    # 2x oversampling
    traj_rad2 = B.scale(0.5, traj_rad)

    # simulate num_chan-channel k-space data
    num_chan = 8
    ksp_sim = B.phantom(k=True, s=num_chan, t=traj_rad2)

    # increase the reconstructed FOV a bit
    traj_rad2 = B.scale(0.6, traj_rad)

    # inverse gridding
    igrid = B.nufft(ksp_sim, i=True, t=traj_rad2)

    # channel combination
    reco1 = B.rss(num_chan, igrid)

    # reconstruct low-resolution image and transform back to k-space
    lowres_img = B.nufft(ksp_sim, i=True, d=[24, 24, 1], t=traj_rad2)
    lowres_ksp = B.fft(lowres_img, u=7)

    # zeropad to full size
    ksp_zerop = B.resize(lowres_ksp, c=(0, 308, 1, 308))

    # ESPIRiT calibration
    sens = B.ecalib(ksp_zerop, m=1)

    # non-Cartesian parallel imging
    reco2 = B.pics(ksp_sim, sens, S=True, r=0.001, t=traj_rad2)
    reco3 = B.pics(ksp_sim, sens, l1=True, S=True, r=0.005, m=True,
                   t=traj_rad2)
    view(np.squeeze(np.concatenate((reco1, reco2, reco3))))
