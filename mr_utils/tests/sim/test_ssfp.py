import unittest
import numpy as np
import matplotlib.pyplot as plt

class DictionaryTestCase(unittest.TestCase):

    def setUp(self):
        self.TR = 6e-6
        self.T1s = np.linspace(0,1,11)[1:] # T1 can't be 0
        self.T2s = np.linspace(0,1,11)[1:] # T2 can't be 0
        self.alphas = np.linspace(np.pi/3,2*np.pi/3,10)
        self.df = np.linspace(-1/self.TR,1/self.TR,100)

    def test_dictionary(self):
        from mr_utils.sim.ssfp import ssfp_dictionary,ssfp_dictionary_for_loop

        # Make sure we get the same answer whether we build dictionary from
        # matrix operations or iterate through a for loop:
        D0,keys0 = ssfp_dictionary(self.T1s,self.T2s,self.TR,self.alphas,self.df)
        D1,keys1 = ssfp_dictionary_for_loop(self.T1s,self.T2s,self.TR,self.alphas,self.df)
        self.assertTrue(np.allclose(D0,D1))

        # # Look at the dictionary
        # plt.plot(np.abs(D0.T))
        # plt.show()

class EllipticalSignalTestCase(unittest.TestCase):

    def setUp(self):
        self.TR = 6e-3
        self.T1,self.T2 = 1,.8
        self.alpha = np.pi/3
        self.df = 100

    def test_ssfp_sim(self):
        from mr_utils.sim.ssfp import ssfp,get_theta,elliptical_params,ssfp_from_ellipse

        # Do it the "normal" way
        I0 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.df)

        # Now do it using the elliptical model
        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        I1 = ssfp_from_ellipse(M,a,b,self.TR,self.df)

        self.assertTrue(np.allclose(I0,I1))

    def test_make_ellipse(self):
        from mr_utils.sim.ssfp import elliptical_params,get_cart_elliptical_params,make_cart_ellipse

        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        xc,yc,A,B = get_cart_elliptical_params(M,a,b)
        x,y = make_cart_ellipse(xc,yc,A,B)

        res = np.zeros(x.shape)
        for ii in range(x.size):
            res[ii] = (x[ii] - xc)**2/A**2 + (y[ii] - yc)**2/B**2

        # (x - xc)**2/A**2 + (y - yc)**2/B**2 == 1
        # Make sure generated x,y satisfy equation for an ellipse
        self.assertTrue(np.allclose(res,np.ones(res.shape)))

    def test_center_of_mass(self):
        from mr_utils.sim.ssfp import elliptical_params,get_center_of_mass,get_center_of_mass_nmr

        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        cm0 = get_center_of_mass(M,a,b)
        cm1 = get_center_of_mass_nmr(self.T1,self.T2,self.TR,self.alpha)

        self.assertTrue(np.allclose(cm0,cm1))

    def test_spectrum(self):
        from mr_utils.sim.ssfp import spectrum

        # This is mostly just to show how it's used
        sig = spectrum(self.T1,self.T2,self.TR,self.alpha)
        # plt.subplot(2,1,1)
        # plt.plot(np.abs(sig))
        # plt.subplot(2,1,2)
        # plt.plot(np.angle(sig))
        # plt.show()

    def test_banding_sim_2d(self):
        from mr_utils.sim.ssfp import ssfp,elliptical_params,ssfp_from_ellipse

        # To get periodic banding like we want to see, we need some serious
        # field inhomogeneity.
        dim = 256
        min_df,max_df = 0,500
        x = np.linspace(min_df,max_df,dim)
        y = np.zeros(dim)
        field_map,_ = np.meshgrid(x,y)

        # # Show the field map
        # plt.imshow(field_map)
        # plt.show()

        # # Generate simulated banding image explicitly using NMR parameters
        sig0 = ssfp(self.T1,self.T2,self.TR,self.alpha,field_map)
        # plt.subplot(2,1,1)
        # plt.imshow(np.abs(sig0))
        # plt.subplot(2,1,2)
        # plt.plot(np.abs(sig0[int(dim/2),:]))
        # plt.show()

        # Generate simulated banding image using elliptical signal model
        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        sig1 =  ssfp_from_ellipse(M,a,b,self.TR,field_map)

        self.assertTrue(np.allclose(sig0,sig1))

if __name__ == '__main__':
    unittest.main()
