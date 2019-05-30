'''Unit tests for composite ellipse construction.'''

import unittest

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.coils.coil_combine import composite_ellipse

class TestCompositeEllipse(unittest.TestCase):
    '''Sanity checks for composite ellipse.'''

    def setUp(self):
        T1 = 1.2
        T2 = .03
        M0 = 1
        TR = 3e-3
        df = 1/(2*TR)
        alpha = np.deg2rad(30)
        npcs = 4
        pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
        ncoils = 5

        # Construct simple coil sensitivities
        mps = np.random.normal(0, 1, ncoils) + 1j*np.mod(
            np.random.normal(0, 1, ncoils), np.pi)

        # Data acquisiton
        self.C = np.zeros((npcs, ncoils), dtype='complex')
        for cc in range(ncoils):
            rf = np.angle(mps[cc])
            self.C[:, cc] = np.abs(mps[cc])*ssfp(
                T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0,
                phi_rf=rf)

    def test_comp_ellipse_no_noise(self):
        '''No noise test.'''
        C0 = composite_ellipse(self.C, coil_axis=-1, disp=True)
        ref_coil = np.argmax(np.max(np.abs(self.C), axis=0))

        # import matplotlib.pyplot as plt
        # plt.plot(self.C[:, ref_coil].real, self.C[:, ref_coil].imag)
        # plt.plot(C0.real, C0.imag, '--')
        # plt.show()
        # print(C0 - self.C[:, ref_coil])

        self.assertTrue(np.allclose(C0, self.C[:, ref_coil]))

    def test_comp_ellipse_with_noise(self):
        '''With noise test.'''

        std = 1e-2
        n_r = np.random.normal(0, std, self.C.shape)
        n_i = np.random.normal(0, std, self.C.shape)
        n = n_r + 1j*n_i
        Cn = self.C + n

        import matplotlib.pyplot as plt
        for cc in range(Cn.shape[1]):
            plt.plot(Cn[:, cc].real, Cn[:, cc].imag)
        plt.show()

        C0 = composite_ellipse(Cn, coil_axis=-1, disp=True)
        ref_coil = np.argmax(np.max(np.abs(Cn), axis=0))

        # import matplotlib.pyplot as plt
        # plt.plot(self.C[:, ref_coil].real, self.C[:, ref_coil].imag)
        # plt.plot(C0.real, C0.imag, '--')
        # plt.show()
        # print(C0 - self.C[:, ref_coil])

        # self.assertTrue(
        #     np.allclose(C0, self.C[:, ref_coil]))
