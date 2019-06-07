'''Use nearest neighbors to estimate the gradient of df.

Notes
-----
Assuming that off-resonance varies smoothly pixel-to-pixel, rf phase
varies smoothly pixel-to-pixel, and that we can segment out similar
tissue, then each nieghboring ellipse should arise from about the same
underlying ellipse, i.e., the tissue properties that define the shape
of the ellipses will be similar.  If we don't expect off-resonance
to vary smoothly, then some other scheme will be required to group
phase-cycle points along the ellipse from adjacent ellipses.

Since we only have 4 points, we cannot specify the ellipse.  But, if
df and rf phase change only a little bit pixel to pixel, then we can
align the ellipses of neighboring pixels and ``fill in'' more points
on the ellipse since df will change where the underlying ellipse was
sampled.  We are effectively using the neighboring ellipses' points to
fully specify our own ellipse.  Now that we have a fully specified
ellipse, we can use a method such as PLANET to get back the
parameters we desire (T1, T2, M0, df, RF phase).

We can actually do something even more interesting, I think...
The rotation required to rotate an ellipse to its neighbor is the
change in off-resonance from the home pixel to the neighboring pixel.
So if we do this for all pixels and their nearest neighbors, we get
4 off-resonance gradient estimates: along each axis and the flipped
version.

If we assume that isocenter has df=0, then we can use a cummulative
sum outward from the isocenter to get off-resonance estimates for
each of our off-resonance gradient estimates (plus some constant --
what it actually was at the isocenter).  We can use this in
conjunction with PLANET to increase the SNR of our resultant
off-resonance maps.

In fact, we can even start reducing the number of phase-cycles
acquired and start filling in all ellipses with the best neighboring
values (the ellipses that most closely match the home ellipse),
hoping that off-resonance will help us out by not being too little or
too large.  So we do require a well-shimmed magnet, I suppose.

After talking with Neal, seems like it becomes less interesting when
you have to rely on other pixels.  Also, off-resonance probably won't
change enough to give a well-conditioned cross-point -- there's a
reason we use evenly spaced phase-cycles.  Maybe applying a shim to
make a large off-resonance across the FOV like we've done before?
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import (
    sos, fit_ellipse_halir, plot_conic)
from mr_utils import view # pylint: disable=W0611

def intersect(P0, P1):
    """P0 and P1 are NxD arrays defining N lines.
    D is the dimension of the space. This function
    returns the least squares intersection of the N
    lines from the system given by eq. 13 in
    http://cal.cs.illinois.edu/~johannes/research/LS_line_intersect.pdf.
    """
    # generate all line direction vectors
    n = (P1 - P0)/np.linalg.norm(P1 - P0, axis=1)[:, None]

    # generate the array of all projectors
    projs = np.eye(n.shape[1]) - n[..., None]*n[:, None] # I - n*n.T

    # generate R matrix and q vector
    R = projs.sum(axis=0)
    q = (projs @ P0[..., None]).sum(axis=0)

    # solve the least squares problem for the
    # intersection point p: Rp = q
    return np.linalg.lstsq(R, q, rcond=None)[0]


if __name__ == '__main__':

    N = 128
    npcs = 2 # how much can we mess around with this...
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    radius = .9
    PD, T1, T2 = cylinder_2d((N, N), radius=radius)
    TR = 3e-3
    alpha = np.deg2rad(70)

    # Quadratic off-resonance, for variety...
    dfx, dfy = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N),
        np.linspace(-1/TR, 1/TR, N))
    df = np.sqrt(dfx**2 + dfy**2)
    # view(df)

    # Try single coil
    I = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=0)
    I4 = ssfp(
        T1, T2, TR, alpha, df,
        phase_cyc=np.linspace(0, 2*np.pi, 4, endpoint=False), M0=PD,
        phi_rf=0)
    if I.ndim == 2:
        I = I[None, ...]
    # view(I)

    # In general, won't be able to lGS right off the bat
    _sos = sos(I, axes=0)
    mask = _sos > .5
    # view(mask)

    # For cross point comparison:
    Itrue = gs_recon(I4, pc_axis=0)

    # Do for each pixel, find the nearest neighbors
    recon = np.zeros((5, N, N), dtype='complex')
    for idx in np.ndindex((N-1, N-1)):
        ii, jj = idx[:]

        x, y = ii+1, jj+1 # home
        xu, yu = x, y+1 # up
        xd, yd = x, y-1 # down
        xl, yl = x-1, y # left
        xr, yr = x+1, y # right

        # Only do pixels that have all the data we need
        if (mask[x, y] and mask[xu, yu] and mask[xl, yl] and
                mask[xr, yr]):

            h = I[:, x, y]
            u = I[:, xu, yu]
            d = I[:, xd, yd]
            l = I[:, xl, yl]
            r = I[:, xr, yr]

            # Center the data
            hm = np.mean(h.real) + 1j*np.mean(h.imag)
            um = np.mean(u.real) + 1j*np.mean(u.imag)
            dm = np.mean(d.real) + 1j*np.mean(d.imag)
            lm = np.mean(l.real) + 1j*np.mean(l.imag)
            rm = np.mean(r.real) + 1j*np.mean(r.imag)
            h = h - hm
            u = u - um
            d = d - dm
            l = l - lm
            r = r - rm

            # Find the correct rotation
            ur = np.angle(
                np.linalg.lstsq(u[:, None], h, rcond=None)[0][0])
            dr = np.angle(
                np.linalg.lstsq(d[:, None], h, rcond=None)[0][0])
            lr = np.angle(
                np.linalg.lstsq(l[:, None], h, rcond=None)[0][0])
            rr = np.angle(
                np.linalg.lstsq(r[:, None], h, rcond=None)[0][0])
            u = u*np.exp(-1j*ur)
            d = d*np.exp(-1j*dr)
            l = l*np.exp(-1j*lr)
            r = r*np.exp(-1j*rr)

            # Put means back where they should be
            h = h + hm
            u = u + um
            d = d + dm
            l = l + lm
            r = r + rm

            # We need to trace out the ellipse in order
            pts = np.array([h, u, d, l, r]).flatten()
            sortid = np.argsort(np.angle(pts))
            coords = pts[sortid]
            xs = coords.real
            ys = coords.imag

            # Try fitting an ellipse, see how it goes
            C = fit_ellipse_halir(xs, ys)
            xe, ye = plot_conic(C)
            plt.plot(xe, ye, ':')

            # # Note: we don't know what the virtual PCs are...
            # # PLANET not working great right now...
            # from mr_utils.recon.ssfp import PLANET
            # Me, T1e, T2e = PLANET(coords, alpha, TR, 1.5)
            # print(Me, T1e, T2e)


            # Show the ellipse
            # for kk in range(coords.size):
            #     plt.plot(xs[kk], ys[kk], '.')
            #     plt.text(xs[kk], ys[kk], '%d' % kk)
            # plt.show()
            plt.plot(h.real, h.imag, '.-')
            plt.plot(u.real, u.imag, '.-')
            plt.plot(d.real, d.imag, '.-')
            plt.plot(l.real, l.imag, '.-')
            plt.plot(r.real, r.imag, '.-')

            # Now we want to find the geometric center of this
            # ellipse
            Itrue0 = Itrue[x, y]
            plt.plot(Itrue0.real, Itrue0.imag, '*')

            plt.axis('square')
            plt.show()
