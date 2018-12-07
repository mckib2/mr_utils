import numpy as np
from mr_utils import view
from mr_utils.recon.reordering import sort2d
from mr_utils.matlab import client_run,client_get,client_put
from mr_utils.load_data import load_mat
from mr_utils.test_data.phantom import bssfp_2d_cylinder
from skimage.measure import compare_mse,compare_ssim,compare_psnr
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def run_ganesh_tcr(kspace,mask,weight_fidelity,weight_temporal,beta_sqrd,noi,reordering=None):

    if reordering is not None:
        client_put({ 'idx_real':reordering.real,'idx_imag':reordering.imag })
        client_run("save('reordering.mat','idx_real','idx_imag')")
        client_run('use_reorder = true;')
    else:
        client_run('use_reorder = false;')

    client_run('clear')
    client_run('pwd')
    client_run('cd mr_utils/recon/reordering/temporal_tv')
    client_put({
        'Coil':kspace,
        'mask_k_space_sparse':mask,
        'weight_fidelity':weight_fidelity,
        'weight_temporal':weight_temporal,
        'beta_sqrd':beta_sqrd,
        'noi':noi
    })
    # client.run('load Coil6.mat; load mask_k_space_sparse.mat')
    client_run('reduced_k_space = Coil.*mask_k_space_sparse;')
    client_run('prior = generate_prior(reduced_k_space);')
    # client.run('recon_data = zeros(size(prior));')
    client_run('recon_data = recon_tcr_reorder(prior,reduced_k_space,mask_k_space_sparse,noi,weight_fidelity,weight_temporal,beta_sqrd,use_reorder);')
    data = client_get([ 'Coil','mask_k_space_sparse','recon_data' ])
    return(data)

def preprocess(data):
    coil_imspace = np.fft.fftshift(np.fft.fft2(data['Coil'],axes=(0,1)),axes=(0,1))
    recon_flipped = np.rot90(np.rot90(data['recon_data'])).astype(coil_imspace.dtype)
    prior = np.fft.fftshift(np.fft.fft2(data['Coil']*data['mask_k_space_sparse'],axes=(0,1)),axes=(0,1))
    return(coil_imspace,recon_flipped,prior)

def do_compare(coil_imspace,recon_flipped):

    # Normalize so they are comparable
    abs_coil_imspace = np.abs(coil_imspace)
    abs_coil_imspace /= np.max(abs_coil_imspace)
    abs_recon_flipped = np.abs(recon_flipped)
    abs_recon_flipped /= np.max(abs_recon_flipped)

    # split into real/imag to do complex MSE
    r_coil_imspace = coil_imspace.real/np.max(np.abs(coil_imspace.real))
    i_coil_imspace = coil_imspace.imag/np.max(np.abs(coil_imspace.imag))
    r_recon_flipped = recon_flipped.real/np.max(np.abs(recon_flipped.real))
    i_recon_flipped = recon_flipped.imag/np.max(np.abs(recon_flipped.imag))

    # Comparisons
    MSE =  1/2*(compare_mse(r_coil_imspace,r_recon_flipped) + compare_mse(i_coil_imspace,i_recon_flipped))
    SSIM = compare_ssim(abs_coil_imspace,abs_recon_flipped)
    PSNR = compare_psnr(abs_coil_imspace,abs_recon_flipped)
    return(MSE,SSIM,PSNR)

if __name__ == '__main__':

    # Make a dynamic phantom
    mask = load_mat('mr_utils/recon/reordering/temporal_tv/mask_k_space_sparse.mat')
    nt,nx,ny = mask.shape[:]

    circ = np.zeros(mask.shape,dtype='complex')
    radius = np.abs(np.sin(np.linspace(0,np.pi,nt))*.7 + .1)
    for ii in range(nt):
        circ[ii,...] = bssfp_2d_cylinder(dims=(nx,ny),radius=radius[ii],kspace=True)
    circ = np.fft.fftshift(circ,axes=(1,2)).transpose((2,1,0))
    mask = mask.transpose(2,1,0)
    # view(mask*circ,fft=True)

    # Run Ganesh's temporal recon
    weight_fidelity = 1.0
    weight_temporal = 0.01
    beta_sqrd = 1e-7
    noi = 200
    # data = run_ganesh_tcr(circ,mask,weight_fidelity,weight_temporal,beta_sqrd,noi)
    #
    # # Unpack, FFT, apply masks to reference, recon, and prior image estimates
    # coil_imspace,recon_flipped,prior = preprocess(data)
    #
    # view(coil_imspace)
    # view(prior)
    # view(recon_flipped)
    #
    # # Do comparisons
    # MSE_no,SSIM_no,PSNR_no = do_compare(coil_imspace,prior)
    # MSE_px,SSIM_px,PSNR_px = do_compare(coil_imspace,recon_flipped)
    #
    # logging.info('For no recon:')
    # logging.info('  MSE : %g' % MSE_no)
    # logging.info('  SSIM: %g' % SSIM_no)
    # logging.info('  PSNR: %g' % PSNR_no)
    #
    # logging.info('For px recon:')
    # logging.info('  MSE : %g' % MSE_px)
    # logging.info('  SSIM: %g' % SSIM_px)
    # logging.info('  PSNR: %g' % PSNR_px)

    # Try patch reordering
    # idx_real = sort2d()
    data = run_ganesh_tcr(circ,mask,weight_fidelity,weight_temporal,beta_sqrd,noi,reordering=None)
