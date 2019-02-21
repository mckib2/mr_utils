'''In vivo proof of concept for fast field mapping for fMRI.

Data:
    10 slices through cerebral cortex, 128x64 (2x in readout), 120 time points,
    4 virtaul coils from 12 channel head coil.  Each successive time point is
    phase-cycled an additional 360/16 = 22.5 degrees leading to 16 groups of
    phase-cycles over the entire 5 minute long readout.  120/5 = 24 time points
    a minute or .4 time points per second or 2.5 seconds per time point.

Experiment:
    Two 10 second blocks -- fixation and flickering checkerboard.  Randomized
    onset with 15 iterations (total 5 minutes).

Considerations:
    Motion in the brain (due to blood flow?) makes distant time points hard to
    compare as pixels don't line up.  To deal with this, short time lengths (N)
    will be used over which we assume there is negligable motion in the brain.
    These are the regions over which parameter maps will be generated.

Method:
    Over N time points, use geometric solution to the elliptical signal model
    to compute banding-free images for these N time points and average all GS
    solutions together.  Small variations due to blood-oxygenation level
    changes induced by the checkerboard are assumed to be averaged over the N
    time points, leaving us with a biased estimator for the banding-free
    images.  How to correct for bias?  Using the averaged GS solutions, we
    compute T1, T2, and alpha maps that we assume to be valid over the N points
    in question.  Then we use these parameter maps to solve for the
    off-resonance maps at each time point n in the set of N time points.  We
    take these off-resonance maps to have BOLD-weighted contrast.
'''

from os.path import dirname, isfile

import numpy as np
from tqdm import trange
from ismrmrdtools.coils import calculate_csm_inati_iter as inati
from skimage.filters import threshold_li

from mr_utils.recon.ssfp import gs_recon3d, PLANET
from mr_utils.utils import sos
from mr_utils import view

if __name__ == '__main__':

    # Load the data
    data_fft_filename = dirname(__file__) + '/data_fft.npy'
    if isfile(data_fft_filename):
        # Go ahead and get the fft'd data directly
        data = np.load(data_fft_filename)
    else:
        # Else we'll have to do it ourselves
        data = np.load(dirname(__file__) + '/data.npy')
        # Put 'er in image space
        print('Starting fft...')
        data = np.fft.fftshift(np.fft.fft2(data, axes=(0, 1)), axes=(0, 1))
        np.save(data_fft_filename, data)
        print('Finished saving fft!')

    # Tell me about it
    print('Data shape is:', data.shape)
    sx, sy, nc, nt, ns = data.shape[:]

    # Take a look at it in all its glory -- notice significant motion
    view(sos(data[..., 1::16, :], axes=2).squeeze(), montage_axis=-1,
         movie_axis=-2)

    # For each coil for all slices for each possible GS recon in N time points
    N = 16  # since we have 16 unique phase-cycles...
    print('Starting GS recons...')
    sh = np.array(data.shape)
    num_gs_recons = int(N/4) # need 4 coil images for GS recon
    sh[3] = num_gs_recons
    recons = np.zeros(sh, dtype=data.dtype)
    for ii in trange(num_gs_recons, desc='GS recons', leave=False):
        for cc in trange(nc, desc='Coils', leave=False):
            ims = data[..., cc, ii:N:4, :]
            recons[..., cc, ii, :] = gs_recon3d(
                *[x.squeeze() for x in np.split(ims, 4, axis=-2)])
    print('Finished GS recons:', recons.shape)

    # Average all the GS recons we got
    recons = np.mean(recons, axis=-2)
    print('Shape of recon after averaging is:', recons.shape)
    view(recons)

    # We still have a coil dimension, can we coil combine here before parameter
    # mapping or is that a no-no?
    _, recons_cc = inati(recons.transpose((2, 0, 1, 3)), smoothing=5, niter=5,
                         thresh=1e-3, verbose=False)
    print('Shape of recon after coil combine is:', recons.shape)

    # Take a look at each slice
    view(recons_cc, montage_axis=-1)

    # For each pixel we want to find T1, T2, so do PLANET on each voxel.  Make
    # a mask using coil combined recons so we only compute voxels in the brain
    thresh = threshold_li(np.abs(recons_cc))
    mask = np.abs(recons_cc) > thresh
    view(mask, montage_axis=-1)

    data_masked = data.transpose((0, 1, 4, 2, 3))
    data_masked = data_masked.reshape((128, 64, 10, -1))
    for ii in range(data_masked.shape[-1]):
        data_masked[..., ii] *= mask
    data_masked = data_masked.reshape((128, 64, 10, 4, 120))
    data_masked = data_masked.transpose((0, 1, 3, 2, 4))
    print('Masked data shape is:', data_masked.shape)
    pcs = [2*np.pi*n/16 for n in range(16)] # Phase cycles
    alpha = np.deg2rad(10)
    TR = 3.34e-3

    # Need to figure out how to only loop over the mask to save on time

    # Choose one slice, one coil to try it out on first N phase-cycles
    coil_idx = 0
    sl_idx = -1
    sl = data_masked[..., coil_idx, sl_idx, :N].squeeze()
    sl_mask = mask[..., sl_idx]
    idx = np.where(sl_mask > 0)
    print(sl.shape)
    pts = sl[idx[0], idx[1], :]
    T2_map = np.zeros(sl_mask.shape)
    for ii in trange(pts.shape[0]):
        try:
            # This is failing because of noise
            _Meff, T1, T2 = PLANET(
                pts[ii, :], alpha, TR, 2, pcs, False, True)
            T2_map[idx[0][ii], idx[1][ii]] = T2
        except AssertionError:
            pass

    view(T2_map)

    # Over the course of these N time points, plot a representative pixel's
    # time curve
    import matplotlib.pyplot as plt
    plt.plot(pcs, sos(data[64, 32, :, :N, :].squeeze(), axes=-3))
    plt.title('Time curves for column of pixels')
    plt.xlabel('Phase-cycle (deg)')
    plt.ylabel('SOS')
    plt.show()
