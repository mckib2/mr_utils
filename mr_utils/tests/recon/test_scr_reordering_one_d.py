import unittest
import numpy as np
import matplotlib.pyplot as plt

class SCRReordering1D(unittest.TestCase):

    def setUp(self):
        pass

    def test_smoothly_varying(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Create a smoothly varying 1D signal
        N = 70
        R = 2 # undersampling factor
        frac = 3/4
        t = np.linspace(-np.pi*frac,np.pi*frac,N)
        sig = np.fft.ifft(np.fft.fft(np.sin(t)*2))

        # Put it in freq domain
        SIG = np.fft.fft(sig)

        # Randomly sample
        np.random.seed(2)
        idx = np.random.permutation(N)
        idx = idx[0:int(N/R)]
        mask = np.zeros(SIG.shape)
        mask[idx] = 1

        # Reconstruct without using reordering
        # Guess on alphas
        recon_no_reorder = scr_reordering_adluru(SIG,mask,alpha0=.0001,alpha1=.05,reorder=False,niters=100).squeeze()
        RECON = np.fft.fft(recon_no_reorder)
        RECON[idx] = SIG[idx]
        recon_no_reorder = np.fft.ifft(RECON)
        self.assertLess(np.sum( np.abs(sig - recon_no_reorder)**2 ),np.sum( np.abs(sig - np.fft.ifft(SIG*mask))**2 ))

        # Reconstruct using reordering
        # alpha0 given in paper, guessing for alpha1
        recon = scr_reordering_adluru(SIG,mask,alpha0=.0035,alpha1=.05,reorder=True,niters=100).squeeze()

        # We do even better if we enforce data consistency at the end!
        RECON = np.fft.fft(recon)
        RECON[idx] = SIG[idx]
        recon = np.fft.ifft(RECON)

        # Make sure we get less error than IFFT and without reordering
        self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - np.fft.ifft(SIG*mask))**2 ))
        self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - recon_no_reorder)**2 ))

        # # Show the result
        # plt.plot(np.abs(sig),label='Orig')
        # plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
        # plt.plot(np.abs(np.abs(recon)),label='SCR')
        # # plt.plot(np.angle(sig)/np.pi,'-.',label='Orig phase')
        # # plt.plot(np.angle(sig)/np.pi,'-.',label='IFFT phase')
        # # plt.plot(np.angle(recon)/np.pi,'--',label='SCR phase')
        # plt.legend()
        # plt.show()

    def test_nonsmoothly_varying(self):
        from mr_utils.recon.reordering import scr_reordering_adluru

        # Create a nonsmoothly varying 1D signal
        N = 70
        R = 2 # undersampling factor
        sig = np.fft.ifft(np.fft.fft(np.random.random(N)))

        # Put it in freq domain
        SIG = np.fft.fft(sig)

        # Randomly sample
        np.random.seed(0)
        idx = np.random.permutation(N)
        idx = idx[0:int(N/R)]
        mask = np.zeros(SIG.shape)
        mask[idx] = 1

        # Reconstruct using TV constraint
        # Just guessing for both alphas...
        recon = scr_reordering_adluru(SIG,mask,alpha0=.0003,alpha1=.08,reorder=True,niters=100).squeeze()

        # We do even better if we enforce data consistency at the end!
        RECON = np.fft.fft(recon)
        RECON[idx] = SIG[idx]
        recon = np.fft.ifft(RECON)

        # Make sure we get less error than IFFT
        self.assertLess(np.sum( np.abs(sig - recon)**2 ),np.sum( np.abs(sig - np.fft.ifft(SIG*mask))**2 ))

        # # Show the result
        # plt.plot(np.abs(sig),label='Orig')
        # plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
        # plt.plot(np.abs(np.abs(recon)),label='SCR')
        # plt.legend()
        # plt.show()



if '__name__' == '__main__':
    unittest.main()
