import unittest
import numpy as np
import matplotlib.pyplot as plt
from mr_utils.recon.util import rmse
from mr_utils.test_data.phantom import bssfp_2d_cylinder
from mr_utils.recon.ssfp import gs_recon
from mr_utils.recon.util import sos,rmse
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

        # params
        self.noise_std = 0
        self.dim = 64
        self.pc_vals = [ 0,np.pi/2,np.pi,3*np.pi/2 ]

        # Find true im by using no noise gs_recon averaged over several
        # different phase-cycles to remove residual banding
        self.true_im = np.zeros((self.dim,self.dim),dtype='complex')
        avgs = [ 0,np.pi/6,np.pi/3,np.pi/4 ]
        for ii,extra in enumerate(avgs):
            pc0 = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=(self.pc_vals[0]+extra),noise_std=0)
            pc1 = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=(self.pc_vals[1]+extra),noise_std=0)
            pc2 = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=(self.pc_vals[2]+extra),noise_std=0)
            pc3 = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=(self.pc_vals[3]+extra),noise_std=0)
            self.true_im += gs_recon(pc0,pc1,pc2,pc3)
        self.true_im /= len(avgs)

        # get simple coil sensitivity maps (1,4,8,16,32 coil combinations)
        dims = (dim,dim)
        self.coil_nums = [ 2,4,8,16,32 ]
        self.csms = []
        for ii,coil_num in enumerate(self.coil_nums):
            # self.csms.append(simple_csm(coil_num,dims))
            self.csms.append(generate_birdcage_sensitivities(dim,number_of_coils=coil_num))

    # def test_walsh(self):
    #     # Make sure we know how to do walsh
    #
    #     err = np.zeros(len(self.csms))
    #     for ii,csm in enumerate(self.csms):
    #         coil_ims = self.im*csm
    #         csm_walsh,rho = calculate_csm_walsh(coil_ims)
    #         im_est = np.sum(csm_walsh*coil_ims,axis=0)
    #
    #         # Compute metrics
    #         err[ii] = rmse(im_est,self.im)
    #
    #     # print(err)
    #
    # def test_inati_iter(self):
    #     # Make sure we know how to do inati
    #
    #     err = np.zeros(len(self.csms))
    #     for ii,csm in enumerate(self.csms):
    #         coil_ims = self.im*csm
    #         csm_inati,im_est = calculate_csm_inati_iter(coil_ims)
    #         # view(csm_inati)
    #
    #         # compute metrics
    #         err[ii] = rmse(im_est,self.im)
    #
    #     # print(err)

    def test_gs_no_combine(self):

        # We want to solve gs_recon for each coil we have in the pc set
        err = []
        for ii,csm in enumerate(self.csms):

            # I have coil sensitivities, now I need an images to apply them to
            # coil_ims: (pc,coil,x,y)
            coil_ims = np.zeros((len(self.pc_vals),csm.shape[0],self.dim,self.dim),dtype='complex')
            for jj,pc in enumerate(self.pc_vals):
                im = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=pc,noise_std=self.noise_std)
                coil_ims[jj,...] = im*csm

            # Now solve for GS for each coil in the phase-cycle sets
            # im_est: (coil,x,y)
            im_est = np.zeros((csm.shape[0],self.dim,self.dim),dtype='complex')
            for kk in range(csm.shape[0]):
                im_est[kk,...] = gs_recon(*[ x.squeeze() for x in np.split(coil_ims[:,kk,...],len(self.pc_vals)) ])
            # view(im_est,phase=True)

            # Combine all the coils using sos and then get the error metric
            im_est_sos = sos(im_est)
            # view(im_est_sos)
            err.append(rmse(im_est_sos,self.true_im))

        # plt.plot(self.coil_nums,err)
        # plt.show()

        # # SOS of the gs solution on each individual coil gives us low periodic
        # # ripple accross the phantom:
        # plt.plot(np.abs(self.true_im[int(self.dim/2),:]))
        # plt.plot(np.abs(im_est_sos[int(self.dim/2),:]))
        # plt.show()

    def test_gs_walsh(self):

        err = []
        for ii,csm in enumerate(self.csms):

            # I have coil sensitivities, now I need an images to apply them to
            # coil_ims: (pc,coil,x,y)
            coil_ims = np.zeros((len(self.pc_vals),csm.shape[0],self.dim,self.dim),dtype='complex')
            for jj,pc in enumerate(self.pc_vals):
                im = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=pc,noise_std=self.noise_std)
                coil_ims[jj,...] = im*csm

            # Callapse the coil dimension of each phase-cycle using Walsh
            pc_est = np.zeros((len(self.pc_vals),self.dim,self.dim),dtype='complex')
            for jj in range(len(self.pc_vals)):
                csm_walsh,_ = calculate_csm_walsh(coil_ims[jj,...])
                pc_est[jj,...] = np.sum(csm_walsh*np.conj(coil_ims[jj,...]),axis=0)
            # view(pc_est,phase=True/)

            # Now that we have combined coils, let's run the single set through
            # gs_recon
            im_est = gs_recon(*[ x.squeeze() for x in np.split(pc_est,len(self.pc_vals)) ])
            # view(im_est)
            err.append(rmse(im_est,self.true_im))

        # plt.plot(self.coil_nums,err)
        # plt.show()

        # # Using Walsh you get same low ripple as with coil by coil
        # plt.plot(np.abs(self.true_im[int(self.dim/2),:]))
        # plt.plot(np.abs(im_est[int(self.dim/2),:]))
        # plt.show()

    def test_gs_inati(self):

        err = []
        for ii,csm in enumerate(self.csms):

            # I have coil sensitivities, now I need an images to apply them to
            # coil_ims: (pc,coil,x,y)
            coil_ims = np.zeros((len(self.pc_vals),csm.shape[0],self.dim,self.dim),dtype='complex')
            for jj,pc in enumerate(self.pc_vals):
                im = bssfp_2d_cylinder(dims=(self.dim,self.dim),phase_cyc=pc,noise_std=self.noise_std)
                coil_ims[jj,...] = im*csm

            # Callapse the coil dimension of each phase-cycle using Walsh
            pc_est = np.zeros((len(self.pc_vals),self.dim,self.dim),dtype='complex')
            for jj in range(len(self.pc_vals)):
                csm_inati,pc_est[jj,...] = calculate_csm_inati_iter(coil_ims[jj,...],smoothing=1)
                # pc_est[jj,...] = np.sum(csm_inati*np.conj(coil_ims[jj,...]),axis=0)
                # view(csm_inati)
            # view(pc_est,phase=True)

            # Now that we have combined coils, let's run the single set through
            # gs_recon
            im_est = gs_recon(*[ x.squeeze() for x in np.split(pc_est,len(self.pc_vals)) ])
            # view(im_est)
            err.append(rmse(im_est,self.true_im))

        # plt.plot(self.coil_nums,err)
        # plt.show()
        #
        # Using Inati
        plt.plot(np.abs(self.true_im[int(self.dim/2),:]))
        plt.plot(np.abs(im_est[int(self.dim/2),:]))
        plt.show()


if __name__ == '__main__':
    unittest.main()
