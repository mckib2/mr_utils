'''Do the same off-resonance mapping but with a phantom data.'''

from os.path import isfile

import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_li
from ismrmrdtools.coils import calculate_csm_walsh
from tqdm import tqdm

from mr_utils.load_data import load_raw
from mr_utils.recon.ssfp import gs_recon
# from mr_utils import view

if __name__ == '__main__':

    # Load in data
    path = '/home/nicholas/Documents/mr_utils/examples/sim/ssfp/'
    file = 'meas_MID38_TRUFI_NBPM_2019_03_22_FID41493.dat'
    if not isfile(path + 'phantom.npy'):
        data = load_raw(path + file, use='rdi')
        np.save(path + 'phantom.npy', data)
    else:
        data = np.load(path + 'phantom.npy')
    print(data.shape)

    file = 'meas_MID39_TRUFI_NBPM_2019_03_22_GRAPPA_R2_FID41494.dat'
    if not isfile(path + 'phantom_grappa.npy'):
        data_grappa = load_raw(path + file, use='rdi')
        np.save(path + 'phantom_grappa.npy', data)
    else:
        data_grappa = np.load(path + 'phantom_grappa.npy')
    print(data_grappa.shape)


    # Dimensions are (avgs, pcs, coils, z, y, x), let's go ahead and
    # collapse the averages dimension
    data = np.mean(data, axis=0)
    data_grappa = np.mean(data, axis=0)

    # Let's put it in image space because that's where we live
    data = np.fft.fftshift(np.fft.fft2(
        data, axes=(-2, -1)), axes=(-2, -1))
    # view(data[:, :, 8, :, :], montage_axis=0, movie_axis=1)

    # For now, let's choose 1 slice
    sl = int(data.shape[2]/2)
    data = data[:, :, sl, :, :]
    # view(data, montage_axis=0, movie_axis=0)

    # Grab all the dimensions
    npcs, ncoils, sx, sy = data.shape[:]

    # Estimate the sensitivity maps from coil images
    M = np.zeros((ncoils, sx, sy), dtype='complex')
    for cc in range(ncoils):
        M[cc, ...] = gs_recon(data[:, cc, ...], pc_axis=0)
    thresh = threshold_li(np.abs(M))
    mask = np.abs(M) > thresh
    mask0 = mask[0, ...]
    csm_est, _ = calculate_csm_walsh(M)
    # view(csm_est*mask)

    # Let's recall the scan parameters
    TR = 5e-3

    # Solve for off-resonance at each voxel
    w0 = np.zeros((sx, sy))
    for idx in tqdm(np.ndindex((sx, sy)), total=sx*sy, leave=False):
        ii, jj = idx[:]
        tmp = np.angle(M[:, ii, jj]) - np.angle(csm_est[:, ii, jj])
        w0[ii, jj] = np.mean(tmp)

    # Convert to Hz
    df_est = w0/(np.pi*TR)
    pad = int(sx/4)
    plt.imshow((df_est*mask0)[pad:-pad, :])
    plt.title('Field Map (Hz)')
    plt.colorbar()
    plt.show()
