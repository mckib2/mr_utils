import numpy as np
import matplotlib.pyplot as plt
from mr_utils import view
from mr_utils.recon.ssfp import gs_recon
from ismrmrdtools.simulation import generate_birdcage_sensitivities
from ismrmrdtools.coils import calculate_csm_walsh,calculate_csm_inati_iter
from mr_utils.recon.util import sos,rmse
from mr_utils.test_data.phantom import bssfp_2d_cylinder

def get_numerical_pahntom_params():

    params = {
        'noise_std': 0,
        'dim': 64,
        'pc_vals': [ 0,np.pi/2,np.pi,3*np.pi/2 ],
        'coil_nums': [ 2,4,8,16,32 ]
    }
    return(params)

def get_true_im_numerical_phantom():

    # Load in params for  simulation
    params = get_numerical_pahntom_params()
    dim = params['dim']
    pc_vals = params['pc_vals']

    # Find true im by using no noise gs_recon averaged over several
    # different phase-cycles to remove residual banding
    true_im = np.zeros((dim,dim),dtype='complex')
    avgs = [ 0,np.pi/6,np.pi/3,np.pi/4 ]
    for ii,extra in enumerate(avgs):
        pc0 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[0] + extra),noise_std=0)
        pc1 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[1] + extra),noise_std=0)
        pc2 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[2] + extra),noise_std=0)
        pc3 = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=(pc_vals[3] + extra),noise_std=0)
        true_im += gs_recon(pc0,pc1,pc2,pc3)
    true_im /= len(avgs)
    return(true_im)

def get_coil_sensitivity_maps():

    # get simple coil sensitivity maps (1,4,8,16,32 coil combinations)
    params = get_numerical_pahntom_params()
    dim = params['dim']
    dims = (dim,dim)
    coil_nums = params['coil_nums']

    csms = []
    for ii,coil_num in enumerate(coil_nums):
        csms.append(generate_birdcage_sensitivities(dim,number_of_coils=coil_num))
    return(csms)

def comparison_numerical_phantom():
    '''Compare coil by coil, Walsh method, and Inati iterative method.
    '''

    true_im = get_true_im_numerical_phantom()
    csms = get_coil_sensitivity_maps()
    params = get_numerical_pahntom_params()
    pc_vals = params['pc_vals']
    dim = params['dim']
    noise_std = params['noise_std']
    coil_nums = params['coil_nums']

    # We want to solve gs_recon for each coil we have in the pc set
    err = np.zeros((3,len(csms)))
    for ii,csm in enumerate(csms):

        # I have coil sensitivities, now I need images to apply them to.
        # coil_ims: (pc,coil,x,y)
        coil_ims = np.zeros((len(pc_vals),csm.shape[0],dim,dim),dtype='complex')
        for jj,pc in enumerate(pc_vals):
            im = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=pc,noise_std=noise_std)
            coil_ims[jj,...] = im*csm


        # Solve the gs_recon coil by coil
        im_est_coils = np.zeros((csm.shape[0],dim,dim),dtype='complex')
        for kk in range(csm.shape[0]):
            im_est_coils[kk,...] = gs_recon(*[ x.squeeze() for x in np.split(coil_ims[:,kk,...],len(pc_vals)) ])
        # Combine all the coils using sos and then get the error metric
        im_est_coils = sos(im_est_coils)

        # Collapse the coil dimension of each phase-cycle using Walsh,Inati
        pc_est_walsh = np.zeros((len(pc_vals),dim,dim),dtype='complex')
        pc_est_inati = np.zeros((len(pc_vals),dim,dim),dtype='complex')
        for jj in range(len(pc_vals)):
            # Walsh
            csm_walsh,_ = calculate_csm_walsh(coil_ims[jj,...])
            pc_est_walsh[jj,...] = np.sum(csm_walsh*np.conj(coil_ims[jj,...]),axis=0)

            # Inati
            csm_inati,pc_est_inati[jj,...] = calculate_csm_inati_iter(coil_ims[jj,...],smoothing=1)

        # Now solve the gs_recon using collapsed coils
        im_est_walsh = gs_recon(*[ x.squeeze() for x in np.split(pc_est_walsh,len(pc_vals)) ])
        im_est_inati = gs_recon(*[ x.squeeze() for x in np.split(pc_est_inati,len(pc_vals)) ])

        # Compute error metrics
        err[0,ii] = rmse(im_est_coils,true_im)
        err[1,ii] = rmse(im_est_walsh,true_im)
        err[2,ii] = rmse(im_est_inati,true_im)

    # # Let's show some stuff
    # plt.plot(coil_nums,err[0,:])
    # plt.plot(coil_nums,err[1,:])
    # plt.plot(coil_nums,err[2,:])
    # plt.show()

    # SOS of the gs solution on each individual coil gives us low periodic
    # ripple accross the phantom, similar to Walsh method:
    plt.plot(np.abs(true_im[int(dim/2),:]))
    plt.plot(np.abs(im_est_coils[int(dim/2),:]))
    plt.plot(np.abs(im_est_walsh[int(dim/2),:]))
    plt.plot(np.abs(im_est_inati[int(dim/2),:]))
    plt.show()

if __name__ == '__main__':
    pass
