import numpy as np
from scipy.misc import factorial
from mr_utils import view
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.field_map import gs_field_map
import matplotlib.pyplot as plt

def acq(field_map,TR=5e-3,alpha=np.deg2rad(10),phase_cyc=0):
    return(ssfp(T1s,T2s,TR,alpha,field_map=field_map,phase_cyc=phase_cyc,M0=PD))

def hdr(t,T0=0,n=4,lam=2):
    # compute the hrf (gamma functions)
    hrf = ((t - T0)**(n - 1))*np.exp(-(t - T0)/lam)/((lam**n)*factorial(n - 1))
    return(hrf)

if __name__ == '__main__':

    # IDEA:
    # - Acquire T1,T2 maps before hand (perhaps during structural scan)
    # - Acquire two phase-cycles per slice, per time point during functional
    # - Use synthetic banding to get two more phase-cycles
    # - Compute field map using elliptical signal model
    # - Compare field maps directly to generate BOLD contrast

    # Simulation
    # - Specify T1,T2 maps
    # - Specify alpha,TR
    # - Change field map in areas that receive blood
    # - Simulate 4 phase-cycled acquisitions
    # - Compute field map
    # - Put field map directly into DICOM
    # - Compute t-tests in AFNI

    # Make a circle brain
    PD,T1s,T2s = cylinder_2d(radius=.8)
    field_map = np.zeros(PD.shape)
    brain = acq(field_map)
    # view(brain)

    # Make HDR
    time_pts = 180
    t = np.linspace(0,20,time_pts)
    hrf = hdr(t)

    # Choose what areas to varying in time
    pd,t1s,t2s = cylinder_2d(radius=.1)
    pd = np.roll(pd,15)
    t1s = np.roll(t1s,-15)
    idx0 = pd > 0
    idx1 = t1s > 0
    idx = idx0 + idx1
    # view(idx1 + idx0 + brain)

    # Make time varying field to simulate blood flow
    tv_field_map = np.zeros(field_map.shape + (time_pts,))
    sigma = .08
    tv_field_map += np.random.normal(0,sigma,tv_field_map.shape)
    tv_field_map[idx,:] += hrf

    # tv_field_map[0,0,:] = 1 # reference scaling pixel
    # view(tv_field_map,movie_axis=-1)

    # Now acquire 4 phase-cycles at each time point
    pc_vals = [ 0,np.pi/2,np.pi,3*np.pi/2 ]
    acqs = np.zeros((len(pc_vals),) + tv_field_map.shape,dtype='complex')
    TR = 5e-4
    for ii in range(time_pts):
        for jj,pc in enumerate(pc_vals):
            acqs[jj,...,ii] = acq(tv_field_map[...,ii],TR=TR,phase_cyc=pc)
    # view(acqs,movie_axis=-1)

    # Now get field maps
    recon_fm = np.zeros(tv_field_map.shape)
    for ii in range(time_pts):
        recon_fm[...,ii] = gs_field_map(*[ x.squeeze() for x in np.split(acqs[...,ii],len(pc_vals)) ],TR=TR)
    # recon_fm[0,0,:] = 1 # ref pixel
    # view(recon_fm,movie_axis=-1)
    # view(np.stack((recon_fm[31,16,:],tv_field_map[31,16,:])))
    plt.subplot(1,2,1)
    plt.plot(np.abs(recon_fm[31,16,:]),label='Recon FM')
    plt.plot(tv_field_map[31,16,:],label='Noisy FM')
    plt.plot(hrf,label='True HDR')
    plt.legend()
    plt.subplot(1,2,2)
    plt.plot(np.abs(recon_fm[31,16,:]),label='Recon FM')
    plt.plot(hrf,label='True HDR')
    plt.legend()
    plt.show()

    # write_dicoms(recon_fm)
