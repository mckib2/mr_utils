'''Load some time curves from real data to examine histograms.'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct

from mr_utils.load_data import load_mat
from mr_utils.cs import ordinator1d
from mr_utils import view

class Sparsify(object):
    '''Picklable sparsifying transform object.'''

    def __init__(self, prior):
        self.x0 = np.atleast_1d(prior[0])

    def forward_fd(self, x):
        '''Sparsifying transform, finite differences.'''
        return np.diff(x)

    def inverse_fd(self, x):
        '''Inverse sparsifying transform, finite differences.'''
        return np.concatenate((self.x0, x)).cumsum()

    def forward_dct(self, x):
        '''Sparsifying transform, discrete cosine transform.'''
        return dct(x, norm='ortho')

    def inverse_dct(self, x):
        '''Inverse sparsifying transform, DCT.'''
        return idct(x, norm='ortho')

if __name__ == '__main__':

    # Load in a data set
    filename = ('/home/nicholas/Documents/research/reordering_data/'
                'STCR_72_rays/Trio/P010710/meas_MID42_CV_Radial7Off_'
                'triple_2.9ml_FID242_GROG.mat')

    data = load_mat(filename, 'Image')
    view(data)
    sx, sy, st, _ = data.shape[:]
    tcurves = data[..., 0].reshape((sx*sy, st))
    view(tcurves[(sx*133 + 130):(sx*133 + 150), :])
    print(tcurves.shape)

    # Pick one pixel we know is going to have a nice time curve
    pt = (133, 130)
    px = data[pt[0], pt[1], :, 0]
    # view(px)

    # # Get orderings for real and imaginary parts
    # sr = Sparsify(px.real)
    # si = Sparsify(px.imag)
    # k = 1
    # rpi = ordinator1d(
    #     px.real, k, sr.inverse_fd, forward=sr.forward_fd, disp=True)
    #
    # plt.plot(px.real, label='Orig')
    # plt.plot(px.real[rpi], label='pi ordered')
    # plt.plot(np.sort(px.real), label='sorted')
    # plt.legend()
    # plt.show()

    # ipi = ordinator1d(
    #     px.imag, k, si.inverse_fd, forward=si.forward_fd, disp=True)
