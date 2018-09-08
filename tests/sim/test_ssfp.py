import unittest
import numpy as np
import matplotlib.pyplot as plt

class EllipticalSignalTestCase(unittest.TestCase):

    def setUp(self):
        self.TR = 6e-3
        self.T1,self.T2 = 1,.8
        self.alpha = np.pi/3

    def test_ssfp_sim(self):
        from sim.ssfp import ssfp,get_theta,elliptical_params,ssfp_from_ellipse

        # Do it the "normal" way
        theta = get_theta(self.TR,100)
        I0 = ssfp(self.T1,self.T2,self.TR,self.alpha,theta)

        # Now do it using the elliptical model
        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        I1 = ssfp_from_ellipse(M,a,b,theta)

        self.assertTrue(np.allclose(I0,I1))

    def test_make_ellipse(self):
        from sim.ssfp import elliptical_params,get_cart_elliptical_params,make_cart_ellipse

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
        from sim.ssfp import elliptical_params,get_center_of_mass,get_center_of_mass_nmr

        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        cm0 = get_center_of_mass(M,a,b)
        cm1 = get_center_of_mass_nmr(self.T1,self.T2,self.TR,self.alpha)

        self.assertTrue(np.allclose(cm0,cm1))

    def test_spectrum(self):
        from sim.ssfp import spectrum

        # This is mostly just to show how it's used
        sig = spectrum(self.T1,self.T2,self.TR,self.alpha)
        plt.subplot(2,1,1)
        plt.plot(np.abs(sig))
        plt.subplot(2,1,2)
        plt.plot(np.angle(sig))
        plt.show()

    def test_banding_sim(self):
        from sim.ssfp import banding_sim_nmr,elliptical_params,banding_sim_elliptical

        # To get periodic banding like we want to see, we need some serious
        # field inhomogeneity.
        dim = 256
        min_df,max_df = 0,500
        x = np.linspace(min_df,max_df,dim)
        y = np.zeros(dim)
        field_map,_ = np.meshgrid(x,y)

        # Show the field map
        # fig, ax = plt.subplots()
        # divider = make_axes_locatable(ax)
        # cax = divider.append_axes('right',size='5%',pad=0.05)
        # im = ax.imshow(field_map)
        # fig.colorbar(im,cax=cax,orientation='vertical')
        # plt.show()

        # Generate simulated banding image explicitly using NMR parameters
        sig0 = banding_sim_nmr(self.T1,self.T2,self.TR,self.alpha,field_map)
        # plt.subplot(2,1,1)
        # plt.imshow(np.angle(sig0))
        # plt.subplot(2,1,2)
        # plt.plot(np.angle(sig0[int(dim/2),:]))
        # plt.show()

        # Generate simulated banding image using elliptical signal model
        M,a,b = elliptical_params(self.T1,self.T2,self.TR,self.alpha)
        sig1 =  banding_sim_elliptical(M,a,b,self.TR,field_map)

        self.assertTrue(np.allclose(sig0,sig1))

if __name__ == '__main__':
    unittest.main()
