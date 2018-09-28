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
        sig = np.sin(t)

        # Put it in freq domain
        SIG = np.fft.fft(sig)

        # Randomly sample
        np.random.seed(2)
        idx = np.random.permutation(N)
        idx = idx[0:int(N/R)]
        mask = np.zeros(SIG.shape)
        mask[idx] = 1

        # Reconstruct using TV constraint
        # alpha0 given in paper, guessing for alpha1
        recon = scr_reordering_adluru(SIG,mask,alpha0=.0035,alpha1=.023,reorder=False,niters=100).squeeze()

        # We do even better if we enforce data consistency at the end!
        RECON = np.fft.fft(recon)
        RECON[idx] = SIG[idx]
        recon = np.fft.ifft(RECON)

        # Show the result
        plt.plot(np.abs(sig),label='Orig')
        plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
        plt.plot(np.abs(np.abs(recon)),label='SCR')
        # plt.plot(np.angle(sig)/np.pi,'-.',label='Orig phase')
        # plt.plot(np.angle(sig)/np.pi,'-.',label='IFFT phase')
        # plt.plot(np.angle(recon)/np.pi,'--',label='SCR phase')
        plt.legend()
        plt.show()


if '__name__' == '__main__':
    unittest.main()
