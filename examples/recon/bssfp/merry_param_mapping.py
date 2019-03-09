'''Parameter mapping for numerical phantom using Taylor method.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.recon.ssfp import taylor_method
from mr_utils.sim.ssfp import ssfp, elliptical_params
from mr_utils.recon.ssfp.merry_param_mapping.plot_ellipse import plotEllipse
from mr_utils import view

if __name__ == '__main__':

    # First initialize everything.
    N = 16
    add_noise = False
    disp = True
    num_pcs = 8
    T1 = np.zeros((N, N))
    T2 = np.zeros((N, N))
    offres = np.zeros((N, N))
    alpha = np.ones((N, N))*np.deg2rad(70) # uniform flip angle across image
    M0 = np.zeros((N, N))

    # Make a simple off-resonance map, linear gradient
    min_df, max_df = 0, 200
    fx = np.linspace(min_df, max_df, N)
    fy = np.zeros(N)
    offres, _ = np.meshgrid(fx, fy)

    # Next set up the desired values across the phantom.  This phantom will be
    # fat on top and water on bottom.
    hi = np.ceil(.9*N).astype(int)
    mid = int(N/2)
    lo = np.floor(.1*N).astype(int)

    # At 3 T fat has a T1 of 300 ms and a T2 of 85 ms. synovial fluid 4813 T1
    # 325 T2
    mask0 = np.zeros((N, N)).astype(bool)
    mask0[lo:mid, lo:hi] = True
    T1[mask0] = 300
    T2[mask0] = 85
    M0[mask0] = 1

    # At 3 T water has a T1 of 3000 ms and a T2 of 160 ms. Cartilage 1568 T1 32
    # T2
    mask1 = np.zeros((N, N)).astype(bool)
    mask1[mid+1:hi, lo:hi] = True
    T1[mask1] = 1200
    T2[mask1] = 30
    M0[mask1] = 1

    # Get effective mask:
    mask = mask0 + mask1
    # view(mask)

    # Set up scan parameters (in milliseconds).
    TR = 10

    # Simulate bSSFP acquisiton at each dphi and get elliptical params, too
    assert np.mod(num_pcs, 4) == 0, ('We should have number of phase cycles'
                                     ' divisible by 4!')
    num_sets = int(num_pcs/4)
    dphis = np.linspace(0, 2*np.pi, num_pcs, endpoint=False)
    Is = []
    a_s = []
    b_s = []
    Ms = []
    for dphi in dphis:
        Is.append(ssfp(
            T1*1e-3, T2*1e-3, TR*1e-3, alpha, offres, phase_cyc=dphi, M0=M0))
        M, a, b = elliptical_params(T1*1e-3, T2*1e-3, TR*1e-3, alpha, M0)
        a_s.append(a)
        b_s.append(b)
        Ms.append(M)

    #--------------------------------------------------------------------------
    # The following code plots four of the phase cycled images.  It is
    # contained within an if block, so if you desire to run it, replace false
    # with true.
    #--------------------------------------------------------------------------
    if disp:
        # Plot the phase cycled images.  For brevity I will only plot the
        # images with 0, 90, 180, and 270 degree phase cycling.
        Is0 = Is[::num_sets]
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.imshow(np.abs(Is0[0]))
        plt.title('0 Degree Phase Cycling')
        plt.subplot(2, 2, 2)
        plt.imshow(np.abs(Is0[1]))
        plt.title('90 Degree Phase Cycling')
        plt.subplot(2, 2, 3)
        plt.imshow(np.abs(Is0[2]))
        plt.title('180 Degree Phase Cycling')
        plt.subplot(2, 2, 4)
        plt.imshow(np.abs(Is0[3]))
        plt.title('270 Degree Phase Cycling')
        plt.show()
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # The following code adds noise to the four phase cycled images used in the
    # elliptical model banding artifact removal.  It is contained in an if
    # block, so if you do not want noise, replace true with false.
    #
    # Also, I use the 0, 90, 180, and 270 degree phase cycled images, but any
    # two pairs of phase cycled images will work, as long as each image is 180
    # degrees offset from its paired image.
    #--------------------------------------------------------------------------
    if add_noise:
        s = 0.001 # std deviation
        for ii, I0 in enumerate(Is):
            n = np.random.normal(
                0, s, I0.shape) + 1j*np.random.normal(0, s, I0.shape)
            Is[ii] += n
    #--------------------------------------------------------------------------

    # Do the mapping
    t1map, t2map, offresmap, m0map = taylor_method(
        Is, dphis, alpha, TR, mask, disp)

    # Show some comparisons
    view(np.stack((offres, offresmap, offres - offresmap)))
    view(np.stack((T1, t1map, T1 - t1map)))
    view(np.stack((T2, t2map, T2 - t2map)))
    view(np.stack((M0, m0map, M0 - m0map)))

    # Compare the ellipses of actual and estimated for one pixel
    if disp:
        # plot ellipse and fit of a pixel
        idx = np.argwhere(mask0)
        idx = idx[np.random.choice(np.arange(idx.shape[0])), :]
        print(idx)
        row, col = idx[0], idx[1]
        xt, yt = plotEllipse(T1[row, col], T2[row, col], TR,
                             alpha[row, col], offres[row, col], M0[row, col],
                             1)
        xe, ye = plotEllipse(t1map[row, col], t2map[row, col], TR,
                             alpha[row, col], offresmap[row, col],
                             m0map[row, col], 1)
        plt.figure()
        plt.plot(xt, yt, 'b')
        plt.plot(xe, ye, 'g--')
        for ii, dphi in enumerate(dphis):
            plt.plot(Is[ii][row, col].real, Is[ii][row, col].imag, 'rx')
        plt.axis('equal')
        plt.show()
