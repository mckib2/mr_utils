import numpy as np
import matplotlib.pyplot as plt
from mr_utils import view
from mr_utils.recon.ssfp import gs_recon
from ismrmrdtools.simulation import generate_birdcage_sensitivities
from ismrmrdtools.coils import calculate_csm_walsh,calculate_csm_inati_iter
from mr_utils.recon.util import sos,rmse
from mr_utils.test_data.phantom import bssfp_2d_cylinder

def get_numerical_phantom_params(SNR=None):

    if SNR is None:
        noise_std = 0
    else:
        im = get_true_im_numerical_phantom()
        m_avg = np.abs(np.nanmean(im[np.nonzero(im)]))
        noise_std = m_avg/SNR

    params = {
        'noise_std': noise_std,
        'dim': 64,
        'pc_vals': [ 0,np.pi/2,np.pi,3*np.pi/2 ],
        'coil_nums': [ 2,4,8,16,32 ]
    }
    return(params)

def get_true_im_numerical_phantom():

    # Load in params for  simulation
    params = get_numerical_phantom_params(SNR=None)
    dim = params['dim']
    pc_vals = params['pc_vals']

    # Find true im by using no noise gs_recon averaged over several
    # different phase-cycles to remove residual banding
    # true_im = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=0)
    true_im = np.zeros((dim,dim),dtype='complex')
    avgs = [ 0,np.pi/6,np.pi/3,np.pi/4 ]
    # avgs = [ 0 ]
    for ii,extra in enumerate(avgs):
        pc0 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[0] + extra))
        pc1 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[1] + extra))
        pc2 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[2] + extra))
        pc3 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[3] + extra))
        true_im += gs_recon(pc0,pc1,pc2,pc3)
    true_im /= len(avgs)
    true_im += 1j*true_im
    # view(np.concatenate((true_im,pc0)))
    return(true_im)

def get_coil_sensitivity_maps():

    # get simple coil sensitivity maps (1,4,8,16,32 coil combinations)
    params = get_numerical_phantom_params()
    dim = params['dim']
    dims = (dim,dim)
    coil_nums = params['coil_nums']

    csms = []
    for ii,coil_num in enumerate(coil_nums):
        csms.append(generate_birdcage_sensitivities(dim,number_of_coils=coil_num))
    return(csms)

def comparison_knee():
    pass

def comparison_numerical_phantom(SNR=None):
    '''Compare coil by coil, Walsh method, and Inati iterative method.'''

    true_im = get_true_im_numerical_phantom()
    csms = get_coil_sensitivity_maps()
    params = get_numerical_phantom_params(SNR=SNR)
    pc_vals = params['pc_vals']
    dim = params['dim']
    noise_std = params['noise_std']
    coil_nums = params['coil_nums']

    # We want to solve gs_recon for each coil we have in the pc set
    err = np.zeros((4,len(csms)))
    for ii,csm in enumerate(csms):

        # I have coil sensitivities, now I need images to apply them to.
        # coil_ims: (pc,coil,x,y)
        coil_ims = np.zeros((len(pc_vals),csm.shape[0],dim,dim),dtype='complex')
        for jj,pc in enumerate(pc_vals):
            im = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=pc)
            im += 1j*im
            coil_ims[jj,...] = im*csm
            coil_ims[jj,...] += np.random.normal(0,noise_std,coil_ims[jj,...].shape) + 1j*np.random.normal(0,noise_std,coil_ims[jj,...].shape)

        # Solve the gs_recon coil by coil
        coil_ims_gs = np.zeros((csm.shape[0],dim,dim),dtype='complex')
        for kk in range(csm.shape[0]):
            coil_ims_gs[kk,...] = gs_recon(*[ x.squeeze() for x in np.split(coil_ims[:,kk,...],len(pc_vals)) ])
        coil_ims_gs[np.isnan(coil_ims_gs)] = 0

        # Easy way out: combine all the coils using sos
        im_est_sos = sos(coil_ims_gs)
        # view(im_est_sos)

        # Take coil by coil solution and do Walsh on it to collapse coil dim
        csm_walsh,_ = calculate_csm_walsh(coil_ims_gs)
        im_est_recon_then_walsh = np.sum(csm_walsh*np.conj(coil_ims_gs),axis=0)
        im_est_recon_then_walsh[np.isnan(im_est_recon_then_walsh)] = 0
        # view(im_est_recon_then_walsh)

        # Collapse the coil dimension of each phase-cycle using Walsh,Inati
        pc_est_walsh = np.zeros((len(pc_vals),dim,dim),dtype='complex')
        pc_est_inati = np.zeros((len(pc_vals),dim,dim),dtype='complex')
        for jj in range(len(pc_vals)):
            ## Walsh
            csm_walsh,_ = calculate_csm_walsh(coil_ims[jj,...])
            pc_est_walsh[jj,...] = np.sum(csm_walsh*np.conj(coil_ims[jj,...]),axis=0)
            # view(csm_walsh)
            # view(pc_est_walsh)

            ## Inati
            csm_inati,pc_est_inati[jj,...] = calculate_csm_inati_iter(coil_ims[jj,...],smoothing=1)
            # pc_est_inati[jj,...] = np.sum(csm_inati*np.conj(coil_ims[jj,...]),axis=0)
            # view(csm_inati)

        # Now solve the gs_recon using collapsed coils
        im_est_walsh = gs_recon(*[ x.squeeze() for x in np.split(pc_est_walsh,len(pc_vals)) ])
        im_est_inati = gs_recon(*[ x.squeeze() for x in np.split(pc_est_inati,len(pc_vals)) ])

        # view(im_est_walsh)
        # view(im_est_recon_then_walsh)

        # Compute error metrics
        err[0,ii] = rmse(im_est_sos,true_im)
        err[1,ii] = rmse(im_est_recon_then_walsh,true_im)
        err[2,ii] = rmse(im_est_walsh,true_im)
        err[3,ii] = rmse(im_est_inati,true_im)

        # view(im_est_inati)

        # # SOS of the gs solution on each individual coil gives us low periodic
        # # ripple accross the phantom, similar to Walsh method:
        # plt.plot(np.abs(true_im[int(dim/2),:]),'--',label='True Im')
        # plt.plot(np.abs(im_est_sos[int(dim/2),:]),'-.',label='SOS')
        # plt.plot(np.abs(im_est_recon_then_walsh[int(dim/2),:]),label='Recon then Walsh')
        # plt.plot(np.abs(im_est_walsh[int(dim/2),:]),label='Walsh then Recon')
        # # plt.plot(np.abs(im_est_inati[int(dim/2),:]),label='Inati')
        # plt.legend()
        # plt.show()


    # Let's show some stuff
    plt.plot(coil_nums,err[0,:],'*-',label='SOS')
    plt.plot(coil_nums,err[1,:],label='Recon then Walsh')
    plt.plot(coil_nums,err[2,:],label='Walsh then Recon')
    # plt.plot(coil_nums,err[3,:],label='Inati')
    plt.legend()
    plt.show()

    return(err)

if __name__ == '__main__':
    pass
