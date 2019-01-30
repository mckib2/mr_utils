'''Port of TVL1denoise - TV-L1 image denoising with the primal-dual algorithm.

See:
https://www.mathworks.com/matlabcentral/fileexchange/57604-tv-l1-image-denoising-algorithm
'''

import numpy as np

#  Copyright (c) 2016 Manolis Lourakis (lourakis **at** ics forth gr)
#  Institute of Computer Science,
#  Foundation for Research & Technology - Hellas
#  Heraklion, Crete, Greece.
#  http://www.ics.forth.gr/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The Software is provided "as is", without warranty of any kind.

def tv_l1_denoise(im, lam, disp=False, niter=100):
    '''TV-L1 image denoising with the primal-dual algorithm.

    im -- image to be processed
    lam -- regularization parameter controlling the amount of denoising;
           smaller values imply more aggressive denoising which tends to
           produce more smoothed results
    disp -- print energy being minimized each iteration
    niter -- number of iterations
    '''

    L2 = 8.0
    tau = 0.02
    sigma = 1.0/(L2*tau)
    theta = 1.0
    lt = lam*tau

    assert im.ndim == 2, 'This function only works for 2D images!'
    height, width = im.shape[:]

    unew = np.zeros(im.shape)
    p = np.zeros((height, width, 2))
    # d = np.zeros(im.shape)
    ux = np.zeros(im.shape)
    uy = np.zeros(im.shape)

    mx = np.max(im)
    if mx > 1.0:
        # normalize
        nim = im/mx
    else:
        # leave intact
        nim = im

    # initialize
    u = nim
    p[:, :, 0] = np.append(u[:, 1:], u[:, -1:], axis=1) - u
    p[:, :, 1] = np.append(u[1:, :], u[-1:, :], axis=0) - u

    # Work out what we're displaying
    if disp:
        from mr_utils.utils.printtable import Table
        table = Table(
            ['Iter', 'Energy'],
            [len(repr(niter)), 8],
            ['d', 'e'])
        print(table.header())
        range_fun = range
    else:
        from tqdm import trange
        range_fun = lambda x: trange(x, leave=False, desc="TV Denoise")

    for kk in range_fun(niter):
        # projection
        # compute gradient in ux, uy
        ux = np.append(u[:, 1:], u[:, -1:], axis=1) - u
        uy = np.append(u[1:, :], u[-1:, :], axis=0) - u
        p += sigma*np.stack((ux, uy), axis=2)

        # project
        normep = np.maximum(np.ones(im.shape),
                            np.sqrt(p[:, :, 0]**2 + p[:, :, 1]**2))
        p[:, :, 0] /= normep
        p[:, :, 1] /= normep

        # shrinkage
        # compute divergence in div
        div = np.vstack((p[:height-1, :, 1], np.zeros((1, width)))) \
            - np.vstack((np.zeros((1, width)), p[:height-1, :, 1]))
        div += np.hstack((p[:, :width-1, 0], np.zeros((height, 1)))) \
            - np.hstack((np.zeros((height, 1)), p[:, :width-1, 0]))

        # TV-L1 model
        v = u + tau*div
        unew = (v - lt)*(v - nim > lt) + (v + lt)*(v - nim < -lt) \
            + nim*(np.abs(v - nim) <= lt)

        # extragradient step
        u = unew + theta*(unew - u)

        # energy being minimized
        if disp:
            E = np.sum(np.sqrt(ux.flatten()**2 + uy.flatten()**2)) \
                + lam*np.sum(np.abs(u.flatten() - nim.flatten()))
            print(table.row((kk, E)))

    newim = u
    return newim

if __name__ == '__main__':
    pass
