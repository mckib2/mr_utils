'''Can we get BART to do reordering?'''

import logging

import numpy as np

from mr_utils.bart import bart
from mr_utils.bart import Bartholomew as B
# from mr_utils.test_data import BARTReordering
from mr_utils import view

if __name__ == '__main__':

    # print(BART_PATH)
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.DEBUG)

    # Generate k-space trajectory with num_spokes radial spokes
    num_spokes = 32
    traj_rad = B.traj(512, num_spokes, r=True)
    logging.info('Generated radial traj with %d spokes', num_spokes)

    # 2x oversampling
    traj_rad2 = B.scale(0.5, traj_rad)
    logging.info('Oversampled by 2')
    # simulate num_chan-channel k-space data
    num_chan = 8
    # ksp_sim = bart(1,'phantom -k -s%d -t' % num_chan,traj_rad2)
    ksp_sim = B.phantom(k=True, s=num_chan, t=traj_rad2)
    logging.info('Simulated %d channel phantom', num_chan)
    # view(ksp_sim)
    # np.save('ksp_sim.npy',ksp_sim)
    # ksp_sim = BARTReordering.ksp_sim()

    # increase the reconstructed FOV a bit
    traj_rad2 = B.scale(0.6, traj_rad)
    logging.info('Increased reconstructed FOV a bit')
    # np.save('traj_rad2.npy',traj_rad2)
    # traj_rad2 = BARTReordering.traj_rad2()

    # inverse gridding
    igrid = bart(1, 'nufft -i -t', traj_rad2, ksp_sim)
    logging.info('NUFFT complete')

    # channel combination
    reco1 = bart(1, 'rss %d' % num_chan, igrid)
    logging.info('RSS completed')
    # np.save('reco1.npy',reco1)
    # reco1 = BARTReordering.reco1()

    # reconstruct low-resolution image and transform back to k-space
    lowres_img = bart(1, 'nufft -i -d24:24:1 -t', traj_rad2, ksp_sim)
    logging.info('Low-res NUFFT complete')
    lowres_ksp = bart(1, 'fft -u 7', lowres_img)
    logging.info('Low-res k-space generated')
    # np.save('lowres_img.npy',lowres_img)
    # np.save('lowres_ksp.npy',lowres_ksp)
    # lowres_img = BARTReordering.lowres_img()
    # lowres_ksp = BARTReordering.lowres_ksp()

    # zeropad to full size
    ksp_zerop = bart(1, 'resize -c 0 308 1 308', lowres_ksp)
    logging.info('k-space zero-padded to full size')

    # ESPIRiT calibration
    sens = bart(1, 'ecalib -m1', ksp_zerop)
    logging.info('ESPIRiT calibration complete')
    # np.save('sens.npy',sens)
    # sens = BARTReordering.sens()

    # non-Cartesian parallel imging
    r = 0.001
    reco2 = bart(1, 'pics -S -r%f -t' % r, traj_rad2, ksp_sim, sens)
    logging.info('PICS with l2 reg (%g) completed', r)

    r = .005
    reco3 = bart(1, 'pics -l1 -S -r%f -m -t' % r, traj_rad2, ksp_sim, sens)
    logging.info('PICS with l1 reg (%g) completed', r)
    # np.save('reco2.npy',reco2)
    # reco2 = BARTReordering.reco2()

    # now try reordering the im-space data according to reco1/reco2/reco3
    ii = np.argsort(np.abs(reco2), axis=0)
    jj = np.arange(reco2.shape[1])
    # reco2_sort = reco2[ii,jj]
    # The problem is that we want to apply the same traj to the fft of
    # reordered image space.  We can do that, we just need to figure out how...
    r = .001
    reco4 = bart(1, 'pics -S -r%f -t' % r, traj_rad2, ksp_sim, sens)
    logging.info(
        'PICS with l2 ref (%g) and reordered according to reco2 completed', r)

    # Take a looksie
    view(np.squeeze(np.stack((reco1, reco2, reco3, reco4))))
