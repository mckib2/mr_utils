'''Use known object in FOV to guide reconstruction.'''

import numpy as np

from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
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
    N = 64
    im = np.rot90(modified_shepp_logan((N, N, 3))[..., 1])
    # view(im)

    # Add a known shape in the empty space, do a cross because it's
    # simple to make
    guide_shape = (5, 5)
    guide = make_cross_guide(guide_shape)
    im[:guide_shape[0], :guide_shape[1]] = guide
    # view(im)

    # Undersample
    num_spokes = 16
    mask = radial(im.shape, num_spokes, skinny=True, extend=True)
    uft = UFT(mask)
    kspace_u = uft.forward_ortho(im)
    view(uft.inverse_ortho(kspace_u))
