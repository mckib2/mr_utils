import unittest
import numpy as np
import matplotlib.pyplot as plt
from mr_utils.sim.traj import radial
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.cs.models import UFT

class TestUFTModel(unittest.TestCase):

    def setUp(self):
        self.N = 10
        self.im = binary_smiley(self.N)
        self.im[:int(self.N/3),:] = 0
        self.num_spokes = 72
        self.samp = radial((self.N,self.N),self.num_spokes,skinny=True)

        # We know this to be correct
        A = np.fft.fftshift(np.fft.fft(np.eye(self.N,self.N)))
        self.E = np.diag(self.samp.flatten()).dot(np.kron(A,A))
        # self.E /= np.sqrt(np.sum(np.abs(self.E)**2,axis=0))

        # This is what we're testing
        self.uft = UFT(self.samp)

    def test_forward(self):

        s0 = self.E.dot(self.im.flatten())
        s = self.uft.dot(self.im.flatten())

        plt.plot(np.abs(s0))
        plt.plot(np.abs(s),'--')
        plt.show()

        # print(s/s0)
        #
        # plt.plot(s0.real)
        # plt.plot(s.real,'--')
        # plt.show()
        #
        # plt.plot(s0.imag)
        # plt.plot(s.imag,'--')
        # plt.show()

    def test_inverse(self):

        s0 = self.E.dot(self.im.flatten())
        m0 = self.E.conj().T.dot(s0)

        s = self.uft.dot(self.im.flatten())
        m = self.uft.conj().T.dot(s)

        plt.plot(np.abs(m0))
        plt.plot(np.abs(m),'--')
        plt.show()

        # plt.plot(m0.real)
        # plt.plot(m.real,'--')
        # plt.show()
        #
        # plt.plot(m0.imag)
        # plt.plot(m.imag,'--')
        # plt.show()


if __name__ == '__main__':
    unittest.main()
