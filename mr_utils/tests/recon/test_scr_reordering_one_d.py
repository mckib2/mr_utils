import unittest
import numpy as np
import matplotlib.pyplot as plt

class SCRReordering1D(unittest.TestCase):

    def setUp(self):
        self.N = 70
        self.R = 2
        frac = 3/4
        self.t = np.linspace(-np.pi*frac,np.pi*frac,self.N)
        self.smooth_sig = np.fft.ifft(np.fft.fft(np.sin(self.t)*2))
        self.smooth_sig_fft = np.fft.fft(self.smooth_sig)

        # Randomly sample
        np.random.seed(0)
        idx = np.random.permutation(self.N)
        idx = idx[0:int(self.N/self.R)]
        self.mask = np.zeros(self.smooth_sig_fft.shape)
        self.mask[idx] = 1

        self.smooth_sig_corrupted = np.fft.ifft(self.smooth_sig_fft*self.mask)

    def test_compare_lasso(self):
        from mr_utils.recon.reordering import scr_reordering_adluru
        from sklearn import linear_model

        reg = linear_model.MultiTaskLasso(alpha=.0001)
        reg.fit(self.t[None,:],np.abs(self.smooth_sig_corrupted)[None,:])
        print(reg)
        recon = reg.coef_.reshape(-1,1)
        print(recon)
        plt.plot(recon)
        plt.show()

        # plt.plot(self.smooth_sig_corrupted.real)
        # plt.plot(self.smooth_sig_corrupted.imag)
        # plt.plot(self.smooth_sig.real)
        # plt.show()


    # def test_smoothly_varying(self):
    #     from mr_utils.recon.reordering import scr_reordering_adluru
    #
    #     # Create a smoothly varying 1D signal
    #     N = 70
    #     R = 2 # undersampling factor
    #     frac = 3/4
    #     t = np.linspace(-np.pi*frac,np.pi*frac,N)
    #     sig = np.fft.ifft(np.fft.fft(np.sin(t)*2))
    #
    #     # Put it in freq domain
    #     SIG = np.fft.fft(sig)
    #
    #     # Randomly sample
    #     np.random.seed(2)
    #     idx = np.random.permutation(N)
    #     idx = idx[0:int(N/R)]
    #     mask = np.zeros(SIG.shape)
    #     mask[idx] = 1
    #
    #     # # Reconstruct without using reordering
    #     # # Guess on alphas
    #     # recon_no_reorder = scr_reordering_adluru(SIG*mask,mask,alpha0=.0001,alpha1=.05,reorder=False,niters=1000).squeeze()
    #     # RECON = np.fft.fft(recon_no_reorder)
    #     # RECON[idx] = SIG[idx]
    #     # recon_no_reorder = np.fft.ifft(RECON)
    #     # # self.assertLess(np.sum( np.abs(sig - recon_no_reorder)**2 ),np.sum( np.abs(sig - np.fft.ifft(SIG*mask))**2 ))
    #
    #     # Reconstruct using reordering
    #     # alpha0 given in paper, guessing for alpha1
    #     recon = scr_reordering_adluru(SIG*mask,mask,alpha0=.00035,alpha1=.005,reorder=True,enforce_consistency=False,niters=1000).squeeze()
    #
    #     # We do even better if we enforce data consistency at the end!
    #     RECON = np.fft.fft(recon)
    #     RECON[idx] = SIG[idx]
    #     recon = np.fft.ifft(RECON)
    #
    #     # Make sure we get less error than IFFT and without reordering
    #     # self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - np.fft.ifft(SIG*mask))**2 ))
    #     # self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - recon_no_reorder)**2 ))
    #
    #     # Show the result
    #     plt.plot(np.abs(sig),label='Orig')
    #     plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
    #     plt.plot(np.abs(np.abs(recon)),label='SCR')
    #     # plt.plot(np.abs(np.abs(recon_no_reorder)),label='SCR (no reorder)')
    #     # plt.plot(np.angle(sig)/np.pi,'-.',label='Orig phase')
    #     # plt.plot(np.angle(sig)/np.pi,'-.',label='IFFT phase')
    #     # plt.plot(np.angle(recon)/np.pi,'--',label='SCR phase')
    #     plt.legend()
    #     plt.show()

    # def test_nonsmoothly_varying(self):
    #     from mr_utils.recon.reordering import scr_reordering_adluru
    #
    #     # Create a nonsmoothly varying 1D signal
    #     N = 70
    #     R = 2 # undersampling factor
    #     np.random.seed(0)
    #     sig = np.fft.ifft(np.fft.fft(np.random.random(N)))
    #
    #     # Put it in freq domain
    #     SIG = np.fft.fft(sig)
    #
    #     # Randomly sample
    #     idx = np.random.permutation(N)
    #     idx = idx[0:int(N/R)]
    #     mask = np.zeros(SIG.shape)
    #     mask[idx] = 1
    #
    #     # Reconstruct using TV constraint
    #     # Just guessing for both alphas...
    #     recon = scr_reordering_adluru(SIG*mask,mask,alpha0=.2,alpha1=.03,reorder=True,niters=1000).squeeze()
    #
    #     # We do even better if we enforce data consistency at the end!
    #     RECON = np.fft.fft(recon)
    #     RECON[idx] = SIG[idx]
    #     recon = np.fft.ifft(RECON)
    #
    #     # Make sure we get less error than IFFT
    #     self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - np.fft.ifft(SIG*mask))**2 ))
    #
    #     # Show the result
    #     plt.plot(np.abs(sig),label='Orig')
    #     plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
    #     plt.plot(np.abs(np.abs(recon)),label='SCR')
    #     plt.legend()
    #     plt.show()

    # def test_reorder_every_iter(self):
    #     from mr_utils.recon.reordering import scr_reordering_adluru
    #
    #     # Create a nonsmoothly varying 1D signal
    #     N = 70
    #     R = 2 # undersampling factor
    #     np.random.seed(0)
    #     sig = np.fft.ifft(np.fft.fft(np.random.random(N)))
    #
    #     # Put it in freq domain
    #     SIG = np.fft.fft(sig)
    #
    #     # Randomly sample
    #     idx = np.random.permutation(N)
    #     idx = idx[0:int(N/R)]
    #     mask = np.zeros(SIG.shape)
    #     mask[idx] = 1
    #
    #     # Reconstruct using TV constraint
    #     # Just guessing for both alphas...
    #     alpha0 = .001
    #     alpha1 = .09
    #     recon = scr_reordering_adluru(SIG*mask,mask,alpha0=alpha0,alpha1=alpha1,reorder=True,reorder_every_iter=False,niters=100).squeeze()
    #     RECON = np.fft.fft(recon)
    #     RECON[idx] = SIG[idx]
    #     recon = np.fft.ifft(RECON)
    #
    #     recon_reorder_every_iter = scr_reordering_adluru(SIG*mask,mask,alpha0=alpha0,alpha1=alpha1,reorder=True,reorder_every_iter=True,niters=100).squeeze()
    #     RECON = np.fft.fft(recon_reorder_every_iter)
    #     RECON[idx] = SIG[idx]
    #     recon_reorder_every_iter = np.fft.ifft(RECON)
    #
    #     # Make sure we get less error
    #     self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - recon_reorder_every_iter)**2 ))
    #
    #     # Show the result
    #     plt.plot(np.abs(sig),label='Orig')
    #     plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
    #     plt.plot(np.abs(np.abs(recon)),label='SCR')
    #     plt.plot(np.abs(np.abs(recon_reorder_every_iter)),label='SCR (reordering every iteration)')
    #     plt.legend()
    #     plt.show()


if '__name__' == '__main__':
    unittest.main()
