import unittest
import numpy as np
from mr_utils.sim.ssfp.gs_coil_combine_comparison import comparison_numerical_phantom,comparison_knee
from mr_utils import view

class GSCoilCombineTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_comparison_numerical_phantom(self):

        ## Notes:
        # Seems to be a tradeoff between Recon->Walsh and Walsh->Recon:
        #     - Walsh->Recon seems to do better with getting edges (try SSIM measure to verify?)
        #     - Recon->Walsh seems to do better with noise
        #
        # Generally...
        #     Recon->Walsh has lower RMSE than Walsh->Recon
        #     SOS RMSE is inbetween Recon->Walsh and Walsh->Recon
        #     Inati is terrible for some reason
        #     Seems like number of coil doesn't do a lot????
        #
        # TODO:
        #     - Monte Carlo MSE for several SNR values
        #     - Discover trends (if any) for number of coils
        #     - Do the same for knee data
        #         - Pay particular attention to smoothness in phase

        err = [] # @ each SNR, rmse for (recon method index,num coils index)
        for SNR in [ None,20,10,5,1 ]:
            err.append(comparison_numerical_phantom(SNR))


    def test_comparison_knee(self):
        comparison_knee()

    # def test_espirit(self):
    #     from mr_utils.recon.espirit import espirit_2d
    #     from ismrmrdtools.simulation import generate_birdcage_sensitivities
    #     from mr_utils.test_data.phantom import bssfp_2d_cylinder
    #
    #     # Grab a sample image
    #     dim = 64
    #     coil_num = 4
    #     csm = generate_birdcage_sensitivities(dim,number_of_coils=coil_num)
    #     im = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=0,noise_std=0)
    #     coil_ims = np.moveaxis(csm*im,0,-1)
    #     view(coil_ims)
    #
    #     Vim,sim = espirit_2d(coil_ims,coil_ims.shape,hkwin_shape=(16,16))
    #
    #     recon = np.sum(np.multiply(coil_ims,np.conj(Vim)),axis=-1)
    #     view(recon)
    #     view(recon[int(dim/2),:])
    #
    #     # recon = Vim*np.conj(coil_ims)
    #     # view(Vim)
    #     # view(sim)

if __name__ == '__main__':
    unittest.main()
