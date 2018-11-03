import unittest
import numpy as np
from mr_utils.recon.util import rmse
# from mr_utils.test_data.coils import simple_csm
# from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils import view
from ismrmrdtools.coils import calculate_csm_walsh,calculate_csm_inati_iter
from ismrmrdtools.simulation import phantom,generate_birdcage_sensitivities

class GSCoilCombineTestCase(unittest.TestCase):

    def setUp(self):

        # load phantom
        dim = 64
        # self.im = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])
        self.im = phantom(dim)

        # get simple coil sensitivity maps (1,4,8,16,32 coil combinations)
        dims = (dim,dim)
        coil_nums = [ 2,4,8,16,32 ]
        self.csms = []
        for ii,coil_num in enumerate(coil_nums):
            # self.csms.append(simple_csm(coil_num,dims))
            self.csms.append(generate_birdcage_sensitivities(dim,number_of_coils=coil_num))

    def test_walsh(self):
        # Make sure we know how to do walsh

        err = np.zeros(len(self.csms))
        for ii,csm in enumerate(self.csms):
            coil_ims = self.im*csm
            csm_walsh,rho = calculate_csm_walsh(coil_ims)
            im_est = np.sum(csm_walsh*coil_ims,axis=0)

            # Compute metrics
            err[ii] = rmse(im_est,self.im)

        # print(err)

    def test_inati_iter(self):
        # Make sure we know how to do inati

        err = np.zeros(len(self.csms))
        for ii,csm in enumerate(self.csms):
            coil_ims = self.im*csm
            csm_inati,im_est = calculate_csm_inati_iter(coil_ims)
            # view(csm_inati)

            # compute metrics
            err[ii] = rmse(im_est,self.im)

        # print(err)

    def test_gs_no_combine(self):
        from mr_utils.test_data.phantom import bssfp_2d_cylinder

        # Try solving GS coil by coil and then combine
        dim = 64
        pcs = np.zeros((4,dim,dim),dtype='complex')
        for ii,pc in enumerate([ 0,np.pi/2,np.pi,3*np.pi/2 ]):
            # pcs[ii,...] = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=pc)
            im = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=pc)

            for jj,csm in enumerate(self.csms):
                coil_ims = im*csm
                # view(coil_ims)

        # view(pcs)

if __name__ == '__main__':
    unittest.main()
