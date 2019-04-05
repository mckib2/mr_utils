'''Do the same off-resonance mapping but with a phantom data.'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_li
from ismrmrdtools.coils import calculate_csm_walsh
from ismrmrdtools.coils import calculate_csm_inati_iter
from tqdm import tqdm, trange
from skimage.restoration import unwrap_phase

from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

if __name__ == '__main__':

    # Load in data
    path = '/home/nicholas/Documents/rawdata/GSFIELDMAP/'
    data = np.load(path + 'set1_fft.npy')
    # Dimensions are (pcs, coils, z, y, x)

    # For now, let's choose 1 slice
    sl = 8
    data = data[:, :, sl, :, :]
    # view(data, montage_axis=0, movie_axis=0)

    # Grab all the dimensions
    npcs, ncoils, sx, sy = data.shape[:]
    pcs = np.linspace(0, 2*np.pi, 4, endpoint=False)
    pcs = np.tile(pcs, (sy, sx, 1)).T

    # Estimate the sensitivity maps from coil images
    # Try espirit
    csm_est = np.load(path + 'csm_P.npy')[
        :, :, sl, :].transpose((2, 0, 1))
    # csm_est = np.load(path + 'csm_P_S.npy')[
    #     :, :, sl, :, 0].transpose((2, 0, 1))
    # print(csm_est.shape)
    # view(csm_est*mask)

    M = np.zeros((ncoils, sx, sy), dtype='complex')
    for cc in range(ncoils):
        M[cc, ...] = gs_recon(data[:, cc, ...], pc_axis=0)
        # M[cc, ...] *= np.exp(1j*pcs[0, ...]/2)
        # view(M[cc, ...])
    thresh = threshold_li(np.abs(M))
    mask = np.abs(M) > thresh
    mask0 = mask[0, ...]
    # csm_est, _ = calculate_csm_walsh(M)
    # csm_est, _ = calculate_csm_inati_iter(M)

    # I think what should actually happen is that coil sensitivity
    # map phase information should be applied to each phase-cycle
    # image before GS recon, then 


    # Let's recall the scan parameters
    TR = 6e-3


    # Comparing to GRE dual echo field map
    gre_fm_c1 = np.load(path + 'fm_c1_s8.npy')
    gre_fm_c2 = np.load(path + 'fm_c2_s8.npy')
    gre_fm_c3 = np.load(path + 'fm_c3_s8.npy')
    gre_fm_c4 = np.load(path + 'fm_c4_s8.npy')
    gre_fm = (gre_fm_c1 + gre_fm_c2 + gre_fm_c3 + gre_fm_c4)/4
    pad = int(sx/4)
    gre_fm = gre_fm[pad:-pad, :]
    mask0 = mask0[pad:-pad, :]

    # # Can we get it right here?
    # M0 = np.sum(csm_est.conj()*M, axis=0)[pad:-pad, :]
    # M0a = np.angle(M0)*mask0
    # M0a = np.fft.fft2(M0a)
    # win = np.kaiser(M0a.shape[0], 5)
    # M0a = np.abs(np.fft.ifft2(M0a*np.outer(win, win)))
    # M0a /= np.pi*TR
    # view(M0a)


    # Solve for off-resonance at each voxel
    #     phi_rf + w0 = angle(M)
    Ma = np.angle(M)[:, pad:-pad, :]
    # view(Ma)
    # Ma = unwrap_phase(Ma)
    # Ma = np.fft.fft2(Ma, axes=(-2, -1))
    # win = np.kaiser(Ma.shape[1], .1)
    # Ma = np.fft.ifft2(Ma*np.outer(win, win), axes=(-2, -1)).real
    # Ma /= np.mean(np.abs(csm_est)[:, pad:-pad, :], axis=0)
    view(Ma)
    # view(Ma)
    csma = np.angle(csm_est)
    csma = csma[:, pad:-pad, :]
    csma = unwrap_phase(csma)
    view(csma)
    print(csma.shape)
    print(Ma.shape)
    x, y = int(265/2), 138
    num = 5
    print(csma[:, x:x+num, y])
    print(Ma[:, x:x+num, y])
    print(csma[:, x:x+num, y] - Ma[:, x:x+num, y])
    print(np.mean(
        csma[:, x:x+num, y] - Ma[:, x:x+num, y], axis=0)/(np.pi*TR))
    print(gre_fm[x:x+num, y])
    w0 = np.mean(Ma + csma, axis=0)

    # Low pass filter to get rid of spurious sign flipping
    w0 = np.fft.fft2(w0)
    win = np.kaiser(w0.shape[0], 14)
    plt.plot(win)
    plt.show()
    w0 = np.abs(np.fft.ifft2(w0*np.outer(win, win)))

    # Convert to Hz
    w0 = unwrap_phase(w0)
    df_est = w0/(np.pi*TR)

    # # Manual unwrapping
    # poss = np.arange(-5, 6).astype(int)
    # fac = 1/(2*TR)
    # for idx, df in tqdm(
    #         np.ndenumerate(df_est), total=df_est.size, leave=False):
    #     ii, jj = idx[:]
    #     cost = np.zeros(poss.size*2)
    #     ll = 0
    #     for kk in range(poss.size):
    #         cost[ll] = gre_fm[ii, jj] - (
    #             df_est[ii, jj] + poss[kk]*fac)
    #         cost[ll+1] = gre_fm[ii, jj] - (
    #             -df_est[ii, jj] + poss[kk]*fac)
    #         ll += 2
    #     nn = np.argmin(np.abs(cost))
    #
    #     modnn = np.mod(nn, 2)
    #     if modnn > 0:
    #         df_est[ii, jj] = -df_est[
    #             ii, jj] + poss[int(nn/2)]*fac
    #     else:
    #         df_est[ii, jj] += poss[int(nn/2)]*fac



    view(np.stack((df_est*mask0, gre_fm*mask0)))
    view((gre_fm - df_est)*mask0)


    plt.imshow((df_est*mask0))
    plt.title('Field Map (Hz)')
    plt.colorbar()
    plt.show()
