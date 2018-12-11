import numpy as np
from scipy.misc import factorial
from scipy.stats import gamma
from mr_utils import view
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.field_map import gs_field_map
from mr_utils.sim.gre import gre_sim
import matplotlib.pyplot as plt
import logging
from tqdm import trange
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=UserWarning)
    import nibabel as nib

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def bssfp_acq(T1s,T2s,PD,field_map,TR=5e-3,alpha=np.deg2rad(10),phase_cyc=0):
    return(ssfp(T1s,T2s,TR,alpha,field_map=field_map,phase_cyc=phase_cyc,M0=PD))

def gre_acq(T1s,T2s,PD,field_map,TR,TE,alpha=np.pi/2):
    return(gre_sim(T1s,T2s,TR=TR,TE=TE,alpha=alpha,field_map=field_map,phi=0,dphi=0,M0=PD,tol=1e-5,iter=None,spoil=True))

def hrf(times):
    '''Return values for HRF at given times

    From:
        http://www.jarrodmillman.com/rcsds/lectures/convolution_background.html
    '''

    # Gamma pdf for the peak
    peak_values = gamma.pdf(times,6)

    # Gamma pdf for the undershoot
    undershoot_values = gamma.pdf(times,12)

    # Combine them
    values = peak_values - 0.35*undershoot_values

    # Scale max to 0.6
    return(values/np.max(values)*0.6)

# def hdr(t,T0=0,n=4,lam=2):
#     # compute the hrf (gamma functions)
#     hrf = ((t - T0)**(n - 1))*np.exp(-(t - T0)/lam)/((lam**n)*factorial(n - 1))
#     return(hrf)

if __name__ == '__main__':

    saveNifti = True
    hrf_scale = .05
    time_pts = 80
    sigma = .25

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
    brain = bssfp_acq(T1s,T2s,PD,field_map)
    # view(brain)

    # Make HDR
    t = np.linspace(0,25,time_pts)
    dt = t[1] - t[0]
    hrf_kernel = hrf(t)*hrf_scale

    # Experiment timing design, assume convolve with BLOCK
    task_lens = [ 20,20 ] # lengths of each task
    reps = 3 # how many repetitions
    times = np.arange(0,np.sum(task_lens)*reps,dt)
    design = np.zeros(times.shape)

    time_ptr = 0
    state = 0
    for ii in range(int(reps*len(task_lens))):
        design[times > time_ptr] = (state % 2)
        time_ptr += task_lens[state % 2]
        state += 1

    # Do the convolution
    hrf0 = np.convolve(design,hrf_kernel)
    design = np.concatenate((design,np.zeros(hrf0.size - design.size)))

    # Now choose only time_pts points
    samples = np.round(np.linspace(0,design.size - 1,time_pts)).astype(int)
    design = design[samples]
    hrf0 = hrf0[samples]

    plt.subplot(1,2,1)
    plt.plot(t,hrf_kernel)
    plt.xlabel('sec')
    plt.title('HRF Model')

    plt.subplot(1,2,2)
    plt.plot(hrf0/hrf_scale,label='Convolved HRF')
    plt.plot(design,label='Block design')
    plt.xlabel('time index')
    plt.legend()
    plt.show()

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
    tv_field_map += np.random.normal(0,sigma,tv_field_map.shape)
    tv_field_map[idx,:] += hrf0

    # tv_field_map[0,0,:] = 1 # reference scaling pixel
    # view(tv_field_map,movie_axis=-1)

    # Now acquire 4 phase-cycles at each time point
    # also get GRE sims for comparison
    pc_vals = [ 0,np.pi/2,np.pi,3*np.pi/2 ]
    bssfp_acqs = np.zeros((len(pc_vals),) + tv_field_map.shape,dtype='complex')
    gre_acqs = np.zeros(tv_field_map.shape,dtype='complex')
    bssfp_TR = 5e-3
    gre_TR = 2.5
    gre_TE = 28e-3
    for ii in trange(time_pts,leave=False):

        gre_acqs[...,ii] = gre_acq(T1s,T2s,PD,tv_field_map[...,ii],TR=gre_TR,TE=gre_TE,alpha=np.pi/2)

        for jj,pc in enumerate(pc_vals):
            bssfp_acqs[jj,...,ii] = bssfp_acq(T1s,T2s,PD,tv_field_map[...,ii],TR=bssfp_TR,phase_cyc=pc)
    # view(acqs,movie_axis=-1)
    view(np.concatenate((gre_acqs,bssfp_acqs[0,...])),movie_axis=-1)

    # Now get field maps
    recon_fm = np.zeros(tv_field_map.shape)
    for ii in range(time_pts):
        recon_fm[...,ii] = gs_field_map(*[ x.squeeze() for x in np.split(bssfp_acqs[...,ii],len(pc_vals)) ],TR=bssfp_TR)
    # recon_fm[0,0,:] = 1 # ref pixel
    # view(recon_fm,movie_axis=-1)
    # view(np.stack((recon_fm[31,16,:],tv_field_map[31,16,:])))
    plt.subplot(1,3,1)
    plt.plot(recon_fm[31,16,:],label='Recon FM')
    plt.plot(tv_field_map[31,16,:],label='Noisy FM')
    plt.plot(hrf0,label='True HDR')
    plt.legend()

    plt.subplot(1,3,2)
    plt.plot(recon_fm[31,16,:],label='Recon FM')
    plt.plot(hrf0,label='True HDR')
    plt.legend()

    plt.subplot(1,3,3)
    plt.plot(np.abs(gre_acqs[31,16,:]),label='GRE')
    plt.legend()
    plt.show()

    if saveNifti:
        # Now we need to stick this data in something AFNI can work with
        data = np.expand_dims(recon_fm,2)
        data = np.stack((data,data),axis=2)
        data += np.min(data)
        img = nib.Nifti1Image(data,np.eye(4))
        filename = 'examples/recon/fmri/bssfp.nii.gz'
        nib.save(img,filename)
        logging.info('Wrote %s with shape %s' % (filename,data.shape))

        data = np.expand_dims(np.abs(gre_acqs),2)
        data = np.stack((data,data),axis=2)
        img = nib.Nifti1Image(data,np.eye(4))
        filename = 'examples/recon/fmri/gre.nii.gz'
        nib.save(img,filename)
        logging.info('Wrote %s with shape %s' % (filename,data.shape))
