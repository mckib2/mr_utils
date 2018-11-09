import numpy as np
import matplotlib.pyplot as plt
from mr_utils import view
from mr_utils.recon.ssfp import gs_recon
from ismrmrdtools.simulation import generate_birdcage_sensitivities
from ismrmrdtools.coils import calculate_csm_walsh,calculate_csm_inati_iter
from mr_utils.recon.util import sos,rmse
from mr_utils.test_data.phantom import bssfp_2d_cylinder
from mr_utils.load_data import load_raw
from scipy.signal import butter, lfilter

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
        # 'coil_nums': [ 2,4,8,16,32 ]
        'coil_nums': [ 16 ]
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

# Metric will be percent ripple
def ripple(im0):
    im = im0.copy()

    # We only want one line through image
    line = im[:,int(im.shape[1]/2)]
    line = line[np.abs(line) > np.max(np.abs(line))/10]

    # Choose a "patch" of the line over distance you assume to be linear
    # and get the ripple for each patch
    pad = 6
    val = []
    for ii in range(np.mod(line.size,pad)):
        line = np.abs(line[ii*6 + int(line.size/2)-pad:ii*6 + int(line.size/2)+pad])
        val.append((np.max(line) - np.min(line))/np.mean(line))

    return(100*np.mean(val))


def ripple_normal(im):
    line = np.abs(im[:,int(im.shape[1]/2)])
    line = line[np.abs(line) > np.max(np.abs(line))/5]
    # view(line)
    val = (np.max(line) - np.min(line))/np.mean(line)
    return(100*val)

def comparison_knee():
    '''Coil by coil, Walsh method, and Inati iterative method for knee data.'''

    # Load the knee data
    dir = '/home/nicholas/Documents/rawdata/SSFP_SPECTRA_dphiOffset_08022018/'
    files = [
        'meas_MID362_TRUFI_STW_TE3_FID29379',
        'meas_MID363_TRUFI_STW_TE3_dphi_45_FID29380',
        'meas_MID364_TRUFI_STW_TE3_dphi_90_FID29381',
        'meas_MID365_TRUFI_STW_TE3_dphi_135_FID29382',
        'meas_MID366_TRUFI_STW_TE3_dphi_180_FID29383',
        'meas_MID367_TRUFI_STW_TE3_dphi_225_FID29384',
        'meas_MID368_TRUFI_STW_TE3_dphi_270_FID29385',
        'meas_MID369_TRUFI_STW_TE3_dphi_315_FID29386'
    ]
    pc_vals = [ 0,45,90,135,180,225,270,315 ]
    dims = (512,256)
    num_coils = 4
    num_avgs = 16

    # # Load in raw once, then save as npy with collapsed avg dimension
    # pcs = np.zeros((len(files),dims[0],dims[1],num_coils),dtype='complex')
    # for ii,file in enumerate(files):
    #     pcs[ii,...] = np.mean(load_raw('%s/%s.dat' % (dir,file),use='s2i'),axis=-1)
    # np.save('%s/te3.npy' % dir,pcs)

    # pcs looks like (pc,x,y,coil)
    pcs = np.load('%s/te3.npy' % dir)
    pcs = np.fft.fftshift(np.fft.fft2(pcs,axes=(1,2)),axes=(1,2))
    # print(pcs.shape)
    # view(pcs,fft=True,montage_axis=0,movie_axis=3)


    # Do recon then coil combine
    coils0 = np.zeros((pcs.shape[-1],pcs.shape[1],pcs.shape[2]),dtype='complex')
    coils1 = coils0.copy()
    for ii in range(pcs.shape[-1]):
        # We have two sets: 0,90,180,27 and 45,135,225,315
        idx0 = [ 0,2,4,6 ]
        idx1 = [ 1,3,5,7 ]
        coils0[ii,...] = gs_recon(*[ x.squeeze() for x in pcs[idx0,:,:,ii] ])
        coils1[ii,...] = gs_recon(*[ x.squeeze() for x in pcs[idx1,:,:,ii] ])
    # Then do the coil combine
    csm_walsh,_ = calculate_csm_walsh(coils0)
    im_est_recon_then_walsh0 = np.sum(csm_walsh*np.conj(coils0),axis=0)
    # view(im_est_recon_then_walsh0)

    csm_walsh,_ = calculate_csm_walsh(coils1)
    im_est_recon_then_walsh1 = np.sum(csm_walsh*np.conj(coils1),axis=0)
    # view(im_est_recon_then_walsh1)

    rip0 = ripple(im_est_recon_then_walsh0)
    rip1 = ripple(im_est_recon_then_walsh1)
    print('recon then walsh: ',np.mean([ rip0,rip1 ]))

    # Now try inati
    csm_inati,im_est_recon_then_inati0 = calculate_csm_inati_iter(coils0,smoothing=5)
    csm_inati,im_est_recon_then_inati1 = calculate_csm_inati_iter(coils1,smoothing=5)
    rip0 = ripple(im_est_recon_then_inati0)
    rip1 = ripple(im_est_recon_then_inati1)
    print('recon then inati: ',np.mean([ rip0,rip1 ]))

    # Now try sos
    im_est_recon_then_sos0 = sos(coils0,axes=0)
    im_est_recon_then_sos1 = sos(coils1,axes=0)
    rip0 = ripple(im_est_recon_then_sos0)
    rip1 = ripple(im_est_recon_then_sos1)
    print('recon then sos: ',np.mean([ rip0,rip1 ]))
    # view(im_est_recon_then_sos)

    ## Now the other way, combine then recon
    pcs0 = np.zeros((2,pcs.shape[0],pcs.shape[1],pcs.shape[2]),dtype='complex')
    pcs1 = pcs0.copy()
    for ii in range(pcs.shape[0]):
        # Walsh it up
        csm_walsh,_ = calculate_csm_walsh(pcs[ii,...].transpose((2,0,1)))
        pcs0[0,ii,...] = np.sum(csm_walsh*np.conj(pcs[ii,...].transpose((2,0,1))),axis=0)
        # view(pcs0[ii,...])

        # Inati it up
        csm_inati,pcs0[1,ii,...] = calculate_csm_inati_iter(pcs[ii,...].transpose((2,0,1)),smoothing=5)

    ## Now perform gs_recon on each coil combined set
    # Walsh
    im_est_walsh_then_recon0 = gs_recon(*[ x.squeeze() for x in pcs0[0,idx0,...] ])
    im_est_walsh_then_recon1 = gs_recon(*[ x.squeeze() for x in pcs0[0,idx1,...] ])
    # Inati
    im_est_inati_then_recon0 = gs_recon(*[ x.squeeze() for x in pcs0[1,idx0,...] ])
    im_est_inati_then_recon1 = gs_recon(*[ x.squeeze() for x in pcs0[1,idx1,...] ])

    # view(im_est_walsh_then_recon0)
    # view(im_est_walsh_then_recon1)
    view(im_est_inati_then_recon0)
    view(im_est_inati_then_recon1)


    rip0 = ripple(im_est_walsh_then_recon0)
    rip1 = ripple(im_est_walsh_then_recon1)
    print('walsh then recon: ',np.mean([ rip0,rip1 ]))

    rip0 = ripple(im_est_inati_then_recon0)
    rip1 = ripple(im_est_inati_then_recon1)
    print('inati then recon: ',np.mean([ rip0,rip1 ]))


    # pcs1[ii,...] = gs_recon(*[ x.squeeze() for x in pcs[idx1,...] ])


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
    err = np.zeros((5,len(csms)))
    rip = err.copy()
    for ii,csm in enumerate(csms):

        # I have coil sensitivities, now I need images to apply them to.
        # coil_ims: (pc,coil,x,y)
        coil_ims = np.zeros((len(pc_vals),csm.shape[0],dim,dim),dtype='complex')
        for jj,pc in enumerate(pc_vals):
            im = bssfp_2d_cylinder(dims=(dim,dim),phase_cyc=pc)
            im += 1j*im
            coil_ims[jj,...] = im*csm
            coil_ims[jj,...] += np.random.normal(0,noise_std,coil_ims[jj,...].shape)/2 + 1j*np.random.normal(0,noise_std,coil_ims[jj,...].shape)/2

        # Solve the gs_recon coil by coil
        coil_ims_gs = np.zeros((csm.shape[0],dim,dim),dtype='complex')
        for kk in range(csm.shape[0]):
            coil_ims_gs[kk,...] = gs_recon(*[ x.squeeze() for x in np.split(coil_ims[:,kk,...],len(pc_vals)) ])
        coil_ims_gs[np.isnan(coil_ims_gs)] = 0

        # Easy way out: combine all the coils using sos
        im_est_sos = sos(coil_ims_gs)
        # view(im_est_sos)

        # Take coil by coil solution and do Walsh on it to collapse coil dim
        # walsh
        csm_walsh,_ = calculate_csm_walsh(coil_ims_gs)
        im_est_recon_then_walsh = np.sum(csm_walsh*np.conj(coil_ims_gs),axis=0)
        im_est_recon_then_walsh[np.isnan(im_est_recon_then_walsh)] = 0
        # view(im_est_recon_then_walsh)

        # inati
        csm_inati,im_est_recon_then_inati = calculate_csm_inati_iter(coil_ims_gs)

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
        err[0,ii] = rmse(im_est_sos,true_im,noroot=True)
        err[1,ii] = rmse(im_est_recon_then_walsh,true_im,noroot=True)
        err[2,ii] = rmse(im_est_recon_then_inati,true_im,noroot=True)
        err[3,ii] = rmse(im_est_walsh,true_im,noroot=True)
        err[4,ii] = rmse(im_est_inati,true_im,noroot=True)

        im_est_sos[np.isnan(im_est_sos)] = 0
        im_est_recon_then_walsh[np.isnan(im_est_recon_then_walsh)] = 0
        im_est_recon_then_inati[np.isnan(im_est_recon_then_inati)] = 0
        im_est_walsh[np.isnan(im_est_walsh)] = 0
        im_est_inati[np.isnan(im_est_inati)] = 0

        rip[0,ii] = ripple_normal(im_est_sos)
        rip[1,ii] = ripple_normal(im_est_recon_then_walsh)
        rip[2,ii] = ripple_normal(im_est_recon_then_inati)
        rip[3,ii] = ripple_normal(im_est_walsh)
        rip[4,ii] = ripple_normal(im_est_inati)

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


    # # Let's show some stuff
    # plt.plot(coil_nums,err[0,:],'*-',label='SOS')
    # plt.plot(coil_nums,err[1,:],label='Recon then Walsh')
    # plt.plot(coil_nums,err[2,:],label='Walsh then Recon')
    # # plt.plot(coil_nums,err[3,:],label='Inati')
    # plt.legend()
    # plt.show()

    print('SOS RMSE:',np.mean(err[0,:]))
    print('recon then walsh RMSE:',np.mean(err[1,:]))
    print('recon then inati RMSE:',np.mean(err[2,:]))
    print('walsh then recon RMSE:',np.mean(err[3,:]))
    print('inati then recon RMSE:',np.mean(err[4,:]))

    print('SOS ripple:',np.mean(err[0,:]))
    print('recon then walsh ripple:',np.mean(rip[1,:]))
    print('recon then inati ripple:',np.mean(rip[2,:]))
    print('walsh then recon ripple:',np.mean(rip[3,:]))
    print('inati then recon ripple:',np.mean(rip[4,:]))

    view(im_est_recon_then_walsh[int(dim/2),:])
    view(im_est_recon_then_inati[int(dim/2),:])
    view(im_est_walsh[int(dim/2),:])
    view(im_est_inati[int(dim/2),:])
    # view(im_est_inati)

    # view(np.stack((im_est_recon_then_walsh,im_est_recon_then_inati,im_est_walsh,im_est_inati)))

    return(err)

if __name__ == '__main__':
    pass
