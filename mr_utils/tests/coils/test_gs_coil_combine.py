'''Remnants from abstract messes...'''

import unittest

# from mr_utils.coils.gs_comparison.gs_coil_combine_comparison import \
    # comparison_knee

class GSCoilCombineTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # def test_comparison_knee(self):
    #
    #     comparison_knee()

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
