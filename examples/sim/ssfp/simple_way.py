'''Use coil sensitivity maps to remove phi_rf dependence.

Notes
-----
This script attempts to correct for phi_rf by adjusting for coil
sensitivities before the GS recon as opposed to after.  I'm not sure
which works better yet.
'''

from os.path import isfile

import numpy as np
from skimage.filters import threshold_li
from skimage.restoration import unwrap_phase
from bart import bart #pylint: disable=E0401

from mr_utils import view
from mr_utils.recon.ssfp import gs_recon

if __name__ == '__main__':

    # Find the data
    path = '/home/nicholas/Documents/rawdata/GSFIELDMAP/'
    file = 'phantom_simple.npy'
    if isfile(path + file):
        im = np.load(path + file)
    else:
        rawname = 'meas_MID69_TRUFI_NBPM_2019_03_22_FID41524.dat'
        data = bart(1, 'twixread -A %s' % (path + rawname))
        print(data.shape)
        data = np.mean(data, axis=-1)
        im = np.fft.fftshift(np.fft.ifft2(
            data, axes=(0, 1)), axes=(0, 1))
        np.save(path + file, im)
    print(im.shape)

    # Get some coil sensitivity maps
    csmfile = 'csm_simple.npy'
    if isfile(path + csmfile):
        csm = np.load(path + csmfile)
    else:
        # kspace = np.fft.fftshift(np.fft.fft2(
        #     np.fft.fftshift(im, axes=(0, 1)), axes=(0, 1)),
        #     axes=(0, 1))
        kspace = np.fft.fft2(im, axes=(0, 1))
        csm = bart(1, 'ecalib -P', kspace)
        csm = np.fft.fftshift(csm, axes=(0, 1))
        np.save(path + csmfile, csm)
    print(csm.shape)

    # Let's do one slice for now
    sl = 8
    im = im[:, :, sl, ...].squeeze()
    csm = csm[:, :, sl, ..., 0].squeeze()
    # view(csm)
    print(im.shape, im.shape)

    # Adjust for coil sensitivities
    im0 = np.zeros((im.shape[:3]), dtype='complex')
    print(im0.shape)
    for ii in range(4):
        im0[..., ii] = np.sum(im[..., :, ii]*csm.conj(), axis=-1)

    # Now do GS recon
    TR = 6e-3
    M = gs_recon(im0, pc_axis=-1)
    m = int(M.shape[0]/4)
    M = M[m:-m, :]
    thresh = threshold_li(np.abs(M))
    mask = np.abs(M) > thresh
    df_est0 = mask*np.angle(M)
    # df_est = unwrap_phase(
    #     np.ma.array(df_est, mask=np.abs(mask - 1)))
    # df_est = np.unwrap(df_est, axis=0)*mask
    # df_est = np.unwrap(df_est, axis=1)*mask

    # win = np.hamming(M.shape[1])
    # win = np.outer(win, win)
    # df_est = np.fft.fft2(df_est)*win
    # df_est = np.fft.ifft2(df_est)
    df_est0 /= np.pi*TR
    # view(df_est0)
    # view(df_est/np.max(np.abs(df_est.flatten())))


    # Try to do GS recon then apply coil sensitivity map
    M0 = np.zeros(im0.shape, dtype='complex')
    for cc in range(im.shape[-2]):
        M0[..., cc] = gs_recon(im[..., cc, :], pc_axis=-1)
    im0 = np.sum(M0*csm.conj(), axis=-1)
    im0 = im0[m:-m, :]
    thresh = threshold_li(np.abs(im0))
    mask = np.abs(im0) > thresh
    df_est1 = mask*np.angle(im0)
    # df_est = unwrap_phase(
    #     np.ma.array(df_est, mask=np.abs(mask - 1)))
    # df_est = np.unwrap(df_est, axis=0)*mask
    # df_est = np.unwrap(df_est, axis=1)*mask
    df_est1 /= np.pi*TR
    # view(df_est1)

    # Mostly the same!
    view(df_est0 - df_est1)
