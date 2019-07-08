'''GCC comparison figure for in vivo brain images.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.test_data import load_test_data
from mr_utils.recon.ssfp import gs_recon
from mr_utils.coils.coil_combine import gcc

if __name__ == '__main__':

    # Load the brain scans
    path = 'mr_utils/test_data/examples/coils/'
    I = load_test_data(path, ['brain_ssfp.npy'])[0]

    # Do some fancy dancing to average all similar phase cycles
    sh = I.shape[:]
    adj = np.mod(sh[-1], 4)
    I = np.reshape(I[..., :-adj], (*sh[:-1], 4, -1))
    I = np.sum(I, axis=-1)
    I = np.moveaxis(I, (-1, -2), (0, 1)) # put axes where we expect

    # We are in k-space, put into image space
    I = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        I, axes=(-2, -1)), axes=(-2, -1)), axes=(-2, -1))

    sl = int(I.shape[2]/4)
    I = I[..., sl:-sl, :]
    npcs, ncoils, sx, sy = I.shape[:]

    # Do coil by coil lGS and then GCC
    lGS = np.zeros((ncoils, sx, sy), dtype='complex')
    for cc in range(ncoils):
        lGS[cc, ...] = gs_recon(I[cc, ...], pc_axis=0)
    lGSgcc = gcc(lGS, coil_axis=0)

    # Now do GCC across coils and do lGS
    I_gcc = np.zeros((npcs, sx, sy), dtype='complex')
    for ii in range(npcs):
        I_gcc[ii, ...] = gcc(I[:, ii, ...], coil_axis=0)
    I_gcc_lGS = gs_recon(I_gcc, pc_axis=0)
    # from mr_utils import view
    # view(np.stack((lGSgcc, I_gcc_lGS)))

    # Now do GCC across coils, substitute phase, and do lGS
    phase = np.zeros((npcs, sx, sy))
    for pc in range(npcs):
        for idx in np.ndindex((sx, sy)):
            ii, jj = idx[:]
            midx = np.argmax(np.abs(I[:, pc, ii, jj]))
            phase[pc, ii, jj] = np.angle(I[midx, pc, ii, jj])
    phase = np.unwrap(phase, axis=0)

    I_gcc_sub = np.abs(I_gcc)*np.exp(1j*phase)
    I_gcc_sub_lGS = gs_recon(I_gcc_sub, pc_axis=0)


    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)


    # Now show the recon results
    args = {
        # 'vmin': 0,
        # 'vmax': 1,
        'cmap': 'gray'
    }
    nx, ny = 2, 3

    # First row
    plt.subplot(nx, ny, 1)
    plt.imshow(np.abs(lGSgcc), **args)
    plt.title('Coil-by-coil lGS + GCC')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.subplot(nx, ny, 2)
    plt.imshow(np.abs(I_gcc_lGS), **args)
    plt.title('Coil-GCC + lGS')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.subplot(nx, ny, 3)
    plt.imshow(np.abs(I_gcc_sub_lGS), **args)
    plt.title('Coil-GCC + phase sub + lGS')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    # Second row
    plt.subplot(nx, ny, 5)
    plt.imshow(np.abs(np.abs(lGSgcc) - np.abs(I_gcc_lGS)), **args)
    plt.ylabel('Residual Error')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.subplot(nx, ny, 6)
    plt.imshow(
        np.abs(np.abs(lGSgcc) - np.abs(I_gcc_sub_lGS)), **args)
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.show()
