import unittest
from mr_utils.coils.coil_combine import coil_pca
from mr_utils.test_data.phantom import bssfp_2d_cylinder
from ismrmrdtools.simulation import generate_birdcage_sensitivities
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import sos
from mr_utils import view
import numpy as np

class TestCoilPCA(unittest.TestCase):

    def setUp(self):
        pass

    def test_simulated_2d(self):

        # Simple numerical phantom
        im0 = bssfp_2d_cylinder(phase_cyc=0)
        im1 = bssfp_2d_cylinder(phase_cyc=np.pi/2)
        im2 = bssfp_2d_cylinder(phase_cyc=np.pi)
        im3 = bssfp_2d_cylinder(phase_cyc=3*np.pi/2)

        # Get coil images
        num_coils = 32
        coil_sens = generate_birdcage_sensitivities(im0.shape[0],number_of_coils=num_coils)
        coil_ims0 = im0*coil_sens
        coil_ims1 = im1*coil_sens
        coil_ims2 = im2*coil_sens
        coil_ims3 = im3*coil_sens

        # Do GS solution to ESM then take SOS
        recon_gs = np.zeros(coil_ims0.shape,dtype='complex')
        for ii in range(num_coils):
            recon_gs[ii,...] = gs_recon(coil_ims0[ii,...],coil_ims1[ii,...],coil_ims2[ii,...],coil_ims3[ii,...])
        recon_gs_sos = sos(recon_gs,axes=(0))
        # view(recon_gs_sos)

        # Do PCA
        n_components = 32
        pca0 = coil_pca(coil_ims0,coil_dim=0,n_components=n_components)
        pca1 = coil_pca(coil_ims1,coil_dim=0,n_components=n_components)
        pca2 = coil_pca(coil_ims2,coil_dim=0,n_components=n_components)
        pca3 = coil_pca(coil_ims3,coil_dim=0,n_components=n_components)

        # Do GS solution to ESM then take SOS, this time using PCA'd data
        recon_pca_gs = np.zeros(pca0.shape,dtype='complex')
        for ii in range(n_components):
            # view(np.concatenate((pca0[ii,...],pca1[ii,...],pca2[ii,...],pca3[ii,...])))
            recon_pca_gs[ii,...] = gs_recon(pca0[ii,...],pca1[ii,...],pca2[ii,...],pca3[ii,...])
        # view(recon_pca_gs)
        recon_pca_gs_sos = sos(recon_pca_gs,axes=(0))
        view(recon_pca_gs_sos)

if __name__ == '__main__':
    unittest.main()
