'''Generate a calibration matrix using BART.'''

from mr_utils.bart import Bartholomew as B
from mr_utils import view

if __name__ == '__main__':

    num_spokes = 32
    traj_rad = B.traj(x=512, y=num_spokes, r=True)
    traj_rad2 = B.scale(0.5, traj_rad)
    num_chan = 8
    ksp_sim = B.phantom(k=True, s=num_chan, t=traj_rad2)
    traj_rad2 = B.scale(0.6, traj_rad)

    calmat = B.calmat(ksp_sim, r=20, k=6)
    U, SV, VH = B.svd(calmat)
    view(SV)

    calib, emaps = B.ecalib(ksp_sim, r=20)
    sens = B.slice((4, 0), calib)
