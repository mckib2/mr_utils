'''Spatially and temporally constrained reconstruction.

Program to reconstruct undersampled DCE MRI data using temporal Total
Variation constraint with reordering.

Notes
-----
Replicates temporal reconstruct results in [1]_.

References
----------
.. [1] G. Adluru, E.V.R. DiBella. Reordering for improved constrained
       reconstruction from undersampled k-space data. International
       Journal of Biomedical Imaging vol. 2008, Article ID 341684,
       12 pages, 2008. doi:10.1155/2008/341684.
'''

import os

import numpy as np

# from mr_utils.cs import GD_temporal_TV
from mr_utils.cs.models import UFT
from mr_utils import view
from mr_utils.load_data import load_mat
# from mr_utils.cs.convex.temporal_gd_tv.generate_prior import generate_prior

if __name__ == '__main__':

    # Parameters for reconstruction
    weight_fidelity = 1
    weight_temporal = 0.01

    # Load in some test data
    path = os.path.dirname(__file__)
    coil = np.load('%s/coil.npy' % path)
    mask = np.load('%s/mask.npy' % path)
    imspace = np.fft.fftshift(np.fft.ifft2(
        coil, axes=(1, 2)), axes=(1, 2))
    # view(imspace)

    # Retrospectively undersample the coil data
    kspace_u = coil*mask
    # print(kspace_u.shape)

    # # Do a naive prior, just the inverse Fourier transform
    # # prior = np.fft.fftshift(np.fft.ifft2(kspace_u, axes=(1, 2)))
    # prior = generate_prior(kspace_u)

    # # Check to make sure we have the right prior
    # path = '/home/nicholas/Downloads/Temporal_reordering/'
    # prior_mat = load_mat('%s/prior.mat' % path, key='prior').T
    # assert np.allclose(prior, prior_mat)
    #
    # # uft = UFT(mask)
    # res = GD_temporal_TV(
    #     prior, kspace_u, mask, weight_fidelity, weight_temporal,
    #     use_reorder=False, beta_sqrd=1e-8, x=imspace, maxiter=200)
    # # print(np.concatenate((res, prior), axis=1).shape)
    #
    # bad = np.fft.fftshift(np.fft.ifft2(kspace_u, axes=(1, 2)), axes=(1, 2))
    # view(np.concatenate(
    #     (imspace, res, prior, bad), axis=1), fft_axes=(1, 2), movie_axis=0)
    #
    # # prior = generate_prior(reduced_k_space)
    # # recon_data = recon_tcr_reorder(prior,reduced_k_space,mask_k_space_sparse,noi,weight_fidelity,weight_temporal,beta_sqrd);
    #
    # # load reduced_data.mat
