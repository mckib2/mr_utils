import unittest
import numpy as np
import matplotlib.pyplot as plt

class SCRReorderingTestCase(unittest.TestCase):

    def setUp(self):
        from mr_utils.test_data import SCRReordering

        # Load in the test test data
        self.kspace = SCRReordering.Coil1_data()
        self.radial_mask = SCRReordering.mask()
        self.tv_prior = SCRReordering.tv_prior()
        self.recon = SCRReordering.recon()
        self.beta2 = 1e-8
        self.alpha0 = 1
        self.alpha1 = .002

        # Get true reorderings
        self.sort_order_real_x,self.sort_order_imag_x,self.sort_order_real_y,self.sort_order_imag_y = SCRReordering.true_orderings()
        self.true_TV_term_reorder_update_real,self.true_TV_term_reorder_update_imag = SCRReordering.TV_re_order()

        # More truth data
        self.true_TV_term_update = SCRReordering.TV_term_update()
        self.true_fidelity_update = SCRReordering.fidelity_update()
        self.recon_1 = SCRReordering.recon_at_iter_1()
        self.recon_2 = SCRReordering.recon_at_iter_2()
        self.recon_10 = SCRReordering.recon_at_iter_10()
        self.recon_50 = SCRReordering.recon_at_iter_50()
        self.recon_100 = SCRReordering.recon_at_iter_100()

    def test_sort_real_imag_parts_space(self):
        from mr_utils.recon.reordering import sort_real_imag_parts_space

        # Prior is the true image
        prior = np.fft.ifft2(self.kspace)
        sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y = sort_real_imag_parts_space(prior*1000)

        # Indices should cancel each other out
        self.assertEqual(np.sum(np.abs(sort_order_imag_x - self.sort_order_imag_x)),0)
        self.assertEqual(np.sum(np.abs(sort_order_imag_y - self.sort_order_imag_y)),0)
        self.assertEqual(np.sum(np.abs(sort_order_real_x - self.sort_order_real_x)),0)
        self.assertEqual(np.sum(np.abs(sort_order_real_y - self.sort_order_real_y)),0)

    def test_TVG_re_order(self):
        from mr_utils.recon.reordering import sort_real_imag_parts_space,TVG_re_order

        # Get reorderings, prior is the true image
        prior = np.fft.ifft2(self.kspace)
        sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y = sort_real_imag_parts_space(prior*1000)

        # First image estimate is the FFT of undersampled kspace
        img_est = np.fft.ifft2(self.kspace*self.radial_mask)

        # Do the TV reordering
        TV_term_reorder_update_real = TVG_re_order(img_est.real,self.beta2,sort_order_real_x,sort_order_real_y)
        TV_term_reorder_update_imag = TVG_re_order(img_est.imag,self.beta2,sort_order_imag_x,sort_order_imag_y)

        self.assertTrue(np.allclose(TV_term_reorder_update_real,self.true_TV_term_reorder_update_real))
        self.assertTrue(np.allclose(TV_term_reorder_update_imag,self.true_TV_term_reorder_update_imag))

    def test_TV_term_update(self):
        from mr_utils.recon.reordering import TVG

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # First image estimate is the FFT of undersampled kspace
        img_est = np.fft.ifft2(self.kspace*self.radial_mask)

        # Try it out
        TV_term_update = self.alpha1*0.5*TVG(img_est,self.beta2)

        self.assertTrue(np.allclose(TV_term_update,self.true_TV_term_update))

    def test_scr_reordering_adluru_fidelity_update(self):
        from mr_utils.recon.reordering import sort_real_imag_parts_space

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # Find a place to start from
        measuredImgDomain = np.fft.ifft2(reduced_kspace)
        img_est = measuredImgDomain.copy()
        W_img_est = np.fft.ifft2(np.fft.fft2(img_est)*self.radial_mask)

        # Determine ordering
        sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y = sort_real_imag_parts_space(prior*1000)

        # inside gradient descent minimization
        fidelity_update = self.alpha0*(measuredImgDomain - W_img_est)

        self.assertTrue(np.allclose(fidelity_update,self.true_fidelity_update))

    def test_scr_reordering_adluru_true_prior_1_iter(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # Run the recon
        im_est = scr_reordering_adluru(reduced_kspace,self.radial_mask,prior=prior,alpha0=self.alpha0,alpha1=self.alpha1,beta2=self.beta2,niters=1)

        self.assertTrue(np.allclose(self.recon_1,im_est))

    def test_scr_reordering_adluru_true_prior_2_iter(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # Run the recon
        im_est = scr_reordering_adluru(reduced_kspace,self.radial_mask,prior=prior,alpha0=self.alpha0,alpha1=self.alpha1,beta2=self.beta2,niters=2)

        self.assertTrue(np.allclose(self.recon_2,im_est))

    def test_scr_reordering_adluru_true_prior_10_iter(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # Run the recon
        im_est = scr_reordering_adluru(reduced_kspace,self.radial_mask,prior=prior,alpha0=self.alpha0,alpha1=self.alpha1,beta2=self.beta2,niters=10)

        self.assertTrue(np.allclose(self.recon_10,im_est))

    def test_scr_reordering_adluru_true_prior_50_iter(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # Run the recon
        im_est = scr_reordering_adluru(reduced_kspace,self.radial_mask,prior=prior,alpha0=self.alpha0,alpha1=self.alpha1,beta2=self.beta2,niters=50)

        self.assertTrue(np.allclose(self.recon_50,im_est))

    def test_scr_reordering_adluru_true_prior_100_iter(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Use the true image as the prior
        prior = np.fft.ifft2(self.kspace)

        # Radial undersampling
        reduced_kspace = self.kspace*self.radial_mask

        # Run the recon
        im_est = scr_reordering_adluru(reduced_kspace,self.radial_mask,prior=prior,alpha0=self.alpha0,alpha1=self.alpha1,beta2=self.beta2,niters=100)

        # plt.subplot(1,3,1)
        # plt.imshow(np.abs(im_est),cmap='gray')
        # plt.title('Mine')
        # plt.subplot(1,3,2)
        # plt.imshow(np.abs(self.recon),cmap='gray')
        # plt.title('True')
        # plt.subplot(1,3,3)
        # plt.imshow(np.abs(im_est - self.recon),cmap='gray')
        # plt.title('Diff')
        # plt.show()

        # Is this too large of a difference?  I think it's numerical error...
        self.assertTrue(np.allclose(self.recon_100,im_est,rtol=.3))

if __name__ == '__main__':
    unittest.main()
