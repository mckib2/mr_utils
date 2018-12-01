import unittest
from sklearn.decomposition import PCA
from skimage.data import lfw_subset
from mr_utils.coils.coil_combine import coil_pca,python_pca
from mr_utils.test_data.phantom import bssfp_2d_cylinder
from ismrmrdtools.simulation import generate_birdcage_sensitivities
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import sos
from mr_utils import view
import numpy as np

class TestPCA(unittest.TestCase):

    def test_python_pca(self):

        dim = 4
        # X = np.random.normal(1,.1,(dim,dim))
        X = lfw_subset()[:10,:,:].reshape((10,-1)).transpose((1,0))
        n_components = 2

        Y_py = python_pca(X,n_components)
        Y_ski = PCA(n_components=n_components,whiten=False).fit_transform(X)
        # print(Y_py)
        # print(Y_ski)

        # Same within scale factor of -1
        self.assertTrue(np.allclose(np.abs(Y_py),np.abs(Y_ski)))

class TestCoilPCA(unittest.TestCase):

    def setUp(self):

        # Simple numerical phantom
        self.im0 = bssfp_2d_cylinder(phase_cyc=0)
        self.im1 = bssfp_2d_cylinder(phase_cyc=np.pi/2)
        self.im2 = bssfp_2d_cylinder(phase_cyc=np.pi)
        self.im3 = bssfp_2d_cylinder(phase_cyc=3*np.pi/2)

        # Get coil images
        self.num_coils = 64
        self.coil_sens = generate_birdcage_sensitivities(self.im0.shape[0],number_of_coils=self.num_coils)
        self.coil_ims0 = self.im0*self.coil_sens
        self.coil_ims1 = self.im1*self.coil_sens
        self.coil_ims2 = self.im2*self.coil_sens
        self.coil_ims3 = self.im3*self.coil_sens

        # Get kspace coil images
        self.kspace_coil_ims0 = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(self.coil_ims0,axes=(1,2)),axes=(1,2)),axes=(1,2))
        self.kspace_coil_ims1 = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(self.coil_ims1,axes=(1,2)),axes=(1,2)),axes=(1,2))
        self.kspace_coil_ims2 = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(self.coil_ims2,axes=(1,2)),axes=(1,2)),axes=(1,2))
        self.kspace_coil_ims3 = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(self.coil_ims3,axes=(1,2)),axes=(1,2)),axes=(1,2))

    def test_simulated_2d(self):


        # # Kind of neat - seeing how phase changes with coil sensitivity...
        # view(np.angle(coil_ims0))

        # Do GS solution to ESM then take SOS
        recon_gs = np.zeros(self.coil_ims0.shape,dtype='complex')
        for ii in range(self.num_coils):
            recon_gs[ii,...] = gs_recon(self.coil_ims0[ii,...],self.coil_ims1[ii,...],self.coil_ims2[ii,...],self.coil_ims3[ii,...])
        # view(np.angle(recon_gs)) # realize this is actually a movie - they all just look the same...
        recon_gs_sos = sos(recon_gs,axes=(0))
        view(recon_gs_sos)

        # Do PCA
        n_components = 4
        pca0 = coil_pca(self.coil_ims0,coil_dim=0,n_components=n_components)
        pca1 = coil_pca(self.coil_ims1,coil_dim=0,n_components=n_components)
        pca2 = coil_pca(self.coil_ims2,coil_dim=0,n_components=n_components)
        pca3,expl_var = coil_pca(self.coil_ims3,coil_dim=0,n_components=n_components,give_explained_var=True)
        # view(expl_var.real)

        # view(np.angle(pca3))

        # Do GS solution to ESM then take SOS, this time using PCA'd data
        recon_pca_gs = np.zeros(pca0.shape,dtype='complex')
        for ii in range(n_components):
            # view(np.concatenate((pca0[ii,...],pca1[ii,...],pca2[ii,...],pca3[ii,...])))
            recon_pca_gs[ii,...] = gs_recon(pca0[ii,...],pca1[ii,...],pca2[ii,...],pca3[ii,...])
        # view(np.angle(recon_pca_gs))
        recon_pca_gs_sos = sos(recon_pca_gs,axes=(0))
        # view(recon_pca_gs_sos)


    def test_simulated_2d_kspace(self):

        # Do PCA on kspace
        n_components = 4
        pca0 = coil_pca(self.kspace_coil_ims0,coil_dim=0,n_components=n_components)
        pca1 = coil_pca(self.kspace_coil_ims1,coil_dim=0,n_components=n_components)
        pca2 = coil_pca(self.kspace_coil_ims2,coil_dim=0,n_components=n_components)
        pca3,expl_var = coil_pca(self.kspace_coil_ims3,coil_dim=0,n_components=n_components,give_explained_var=True)
        # view(expl_var.imag)

        # Put it back in image space
        pca0 = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(pca0,axes=(1,2)),axes=(1,2)),axes=(1,2))
        pca1 = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(pca1,axes=(1,2)),axes=(1,2)),axes=(1,2))
        pca2 = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(pca2,axes=(1,2)),axes=(1,2)),axes=(1,2))
        pca3 = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(pca3,axes=(1,2)),axes=(1,2)),axes=(1,2))

        # Do GS solution to ESM then take SOS, this time using PCA'd data
        recon_pca_gs = np.zeros(pca0.shape,dtype='complex')
        for ii in range(n_components):
            # view(np.concatenate((pca0[ii,...],pca1[ii,...],pca2[ii,...],pca3[ii,...])))
            recon_pca_gs[ii,...] = gs_recon(pca0[ii,...],pca1[ii,...],pca2[ii,...],pca3[ii,...])
        # view(np.angle(recon_pca_gs))
        recon_pca_gs_sos = sos(recon_pca_gs,axes=(0))
        # view(recon_pca_gs_sos)


if __name__ == '__main__':
    unittest.main()
