import numpy as np
from mr_utils.test_data import SCRReordering
from mr_utils import view
from mr_utils.cs import GD_TV
from mr_utils.cs.models import UFT
from skimage.filters import gaussian
from skimage.measure import compare_mse,compare_ssim

if __name__ == '__main__':

    # We need a mask
    mask = np.fft.fftshift(SCRReordering.mask())

    # Get the encoding model
    uft = UFT(mask)

    # Load in the test data
    kspace = np.fft.fftshift(SCRReordering.Coil1_data())
    imspace = uft.inverse(kspace)

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = uft.inverse(kspace_u)

    # Do reconstruction using gradient descent without reordering
    do_reordering = False
    x_hat_wo = GD_TV(kspace_u,forward_fun=uft.forward,inverse_fun=uft.inverse,alpha=.5,lam=.004,do_reordering=do_reordering,x=imspace,ignore_residual=True,disp=False,maxiter=50)

    # Do reconstruction using gradient descent with reordering
    do_reordering = True
    x_hat_w = GD_TV(kspace_u,forward_fun=uft.forward,inverse_fun=uft.inverse,alpha=.5,lam=.004,do_reordering=do_reordering,x=imspace,ignore_residual=True,disp=False,maxiter=50)

    # Try iterating on it:
    x_hat_iter = imspace_u.copy()
    sigma = 100
    beta = .8
    iters = 30
    lam = .004

    ims = np.zeros(((iters,) + imspace_u.shape),dtype='complex')
    ssim = np.zeros(iters)
    err = np.zeros(iters)
    absimage = np.abs(imspace)

    for ii in range(iters):
        prior = gaussian(x_hat_iter.real,np.sqrt(sigma)) + 1j*gaussian(x_hat_iter.imag,np.sqrt(sigma))
        # prior = gaussian(np.abs(x_hat_iter),sigma)*np.exp(-1j*np.angle(x_hat_iter))
        x_hat_iter = GD_TV(kspace_u,forward_fun=uft.forward,inverse_fun=uft.inverse,alpha=.5,lam=lam,do_reordering=True,x=prior,ignore_residual=True,disp=False,maxiter=50)
        sigma *= beta
        # lam /= beta

        err[ii] = compare_mse(absimage,np.abs(x_hat_iter))
        ssim[ii] = compare_ssim(absimage,np.abs(x_hat_iter))
        ims[ii,...] = x_hat_iter#*beta
        print(ii,err[ii],ssim[ii])
    # recon = np.mean(ims,axis=0)
    recon = ims[-1,...]

    view(err)
    view(ssim)
    # view(np.stack((np.mean(ims[:-1,...],axis=0),x_hat_iter,x_hat_w,x_hat_wo,imspace)))

    print('No reordering  ',np.linalg.norm(imspace/np.linalg.norm(imspace) - x_hat_wo/np.linalg.norm(x_hat_wo)))
    print('Iterated       ',np.linalg.norm(imspace/np.linalg.norm(imspace) - recon/np.linalg.norm(recon)))
    print('True reordering',np.linalg.norm(imspace/np.linalg.norm(imspace) - x_hat_w/np.linalg.norm(x_hat_w)))


    view(imspace/np.linalg.norm(imspace) - recon/np.linalg.norm(recon))
    view(imspace/np.linalg.norm(imspace) - x_hat_w/np.linalg.norm(x_hat_w))
    view(np.stack((recon/np.linalg.norm(recon),x_hat_w/np.linalg.norm(x_hat_w))))
