import unittest
import numpy as np
import matplotlib.pyplot as plt

class SCRReordering1D(unittest.TestCase):

    def setUp(self):
        pass

    def test_smoothly_varying(self):
        from mr_utils.recon.reordering import scr_reordering_adluru
        from scipy.optimize import minimize

        # Create a smoothly varying 1D signal
        N = 5000
        R = 2 # undersampling factor
        frac = 3/4
        t = np.linspace(-np.pi*frac,np.pi*frac,N)
        sig = np.sin(t)

        # Put it in freq domain
        SIG = np.fft.fft(sig)
        SIG = SIG[:,None]

        # Randomly sample
        np.random.seed(1)
        idx = np.random.permutation(N)
        idx = idx[0:int(N/R)]
        mask = np.zeros(SIG.shape)
        mask[idx] = 1

        # Reconstruct using TV constraint
        recon = scr_reordering_adluru(SIG,mask,reorder=False)

        plt.plot(sig,label='Orig')
        plt.plot(np.abs(np.fft.ifft(SIG*mask)),label='IFFT')
        plt.plot(np.abs(recon),label='SCR')
        plt.legend()
        plt.show()





if '__name__' == '__main__':
    unittest.main()
