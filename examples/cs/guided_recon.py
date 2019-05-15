'''Use known object in FOV to guide reconstruction.'''

import numpy as np
from skimage.measure import compare_mse
from scipy.optimize import line_search, minimize

from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.utils import dTV
from mr_utils import view

def make_cross_guide(shape):
    '''Make a cross of size shape to guide image reconstruction.'''
    guide = np.zeros(shape)
    guide_center = [int(xx/2) for xx in shape[:]]
    guide[guide_center[0], :] = 1
    guide[:, guide_center[1]] = 1
    return guide

if __name__ == '__main__':

    # Get ol' Shepp-logan up and running
    N = 128
    im = np.rot90(modified_shepp_logan((N, N, 3))[..., 1])
    # view(im)

    # Add a known shape in the empty space, do a cross because it's
    # simple to make
    guide_shape = (15, 15)
    guide = make_cross_guide(guide_shape)
    im[:guide_shape[0], :guide_shape[1]] = guide
    # view(im)

    # Undersample
    num_spokes = 16
    mask = radial(im.shape, num_spokes, skinny=True, extend=True)
    uft = UFT(mask)
    kspace_u = uft.forward_ortho(im)
    imspace_u = uft.inverse_ortho(kspace_u)

    # Simple gradient descent algorithm
    done = False
    imhat = uft.inverse_ortho(kspace_u)
    maxiter = 1500
    # lam0 = 2
    lam1 = .003
    err = []

    # Fidelity cost and gradient functions:
    Jf = lambda x0: .5*np.linalg.norm(uft.forward_ortho(
        x0) - kspace_u)
    Jfp = lambda x0: .5*uft.inverse_ortho(
        uft.forward_ortho(x0) - kspace_u)

    # Jtv = lambda x0: np.linalg.norm()

    # imhat = minimize(method='BFGS')

    for ii in range(maxiter):

        # Find update terms
        fidelity = Jfp(imhat)
        tv = dTV(imhat)

        # Find correct weights for each update term
        # ...

        # Take the step
        imhat -= lam0*fidelity + lam1*tv

        # Track error
        err.append(compare_mse(im, np.abs(imhat)))

    view(err)
    view(np.stack((im, imspace_u, imhat)))
