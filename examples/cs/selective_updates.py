import numpy as np
from mr_utils import view
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.cs import proximal_GD
from mr_utils.utils.wavelet import cdf97_2d_forward,cdf97_2d_inverse
from mr_utils.utils.orderings import inverse_permutation,col_stacked_order
from mr_utils.utils.sort2d import sort2d
from skimage.util import view_as_windows
from skimage.measure import compare_mse,compare_ssim

if __name__ == '__main__':

    ## IDEA:
    # Only update areas that we are most confident about at each iteration.

    # Phantom
    N = 2**9
    x = binary_smiley(N)

    # Sampling mask and encoding model
    mask = radial(x.shape,16,extend=True)
    uft = UFT(mask)

    # Sample
    y = uft.forward_ortho(x)

    # Decide how we'll be selective in our updates
    percent_to_keep = .04
    num_to_keep = int(percent_to_keep*y.size)
    def select_n(x_hat,update):
        return(np.unravel_index(np.argpartition(np.abs(x_hat - update).flatten(),-num_to_keep)[-num_to_keep:],x_hat.shape))

    idx = np.arange(y.size).reshape(y.shape)
    idx = view_as_windows(idx,window_shape=128,step=64)
    def select_patch(x_hat,update):
        ii = np.random.randint(0,idx.shape[0])
        jj = np.random.randint(0,idx.shape[1])
        return(np.unravel_index(idx[ii,jj,...],x.shape))

    # Do the recon using wavelet sparsifying transform for each way we're
    # selecting update locations
    maxiter = 20
    alpha = .15
    ignore = True
    disp = False

    # Sparsifying transforms
    level = 5
    wvlt,locations = cdf97_2d_forward(x,level)
    sparsify = lambda x: cdf97_2d_forward(x,level)[0]
    unsparsify = lambda x: cdf97_2d_inverse(x,locations)
    # sparsify = lambda x_hat: np.diff(x_hat)
    # unsparsify = lambda x_hat: np.hstack((x[0,0],x_hat)).cumsum().reshape(x.shape)

    # How should we reorder?
    # _,reordering_r = sort2d(x.real)
    # _,reordering_i = sort2d(x.imag)
    # reordering = reordering_r + 1j*reordering_i
    # def reorder(x_hat):
    #     global reordering
    #     return(reordering)

    # def reorder(x_hat):
    #     _,reordering_r = sort2d(x_hat.real)
    #     _,reordering_i = sort2d(x_hat.imag)
    #     return(reordering_r + 1j*reordering_i)

    reorder = None

    # selectives = [ None,select_n,select_patch ]
    selectives = [ None,select_n ]
    # selectives = [ None ]
    x_hats = np.zeros((len(selectives),) + y.shape,dtype=y.dtype)
    for ii,selective in enumerate(selectives):
        x_hats[ii,...] = proximal_GD(y,forward_fun=uft.forward_ortho,inverse_fun=uft.inverse_ortho,sparsify=sparsify,unsparsify=unsparsify,reorder_fun=reorder,alpha=alpha,selective=selective,x=x,ignore_residual=ignore,disp=disp,maxiter=maxiter)

    for ii,selective in enumerate(selectives):
        if selective is None:
            name = 'None'
        else:
            name = selective.__name__
        print('For %s:' % name)
        print('    Compare  MSE: %g' % compare_mse(np.abs(x_hats[ii,...]),x))
        print('    Compare SSIM: %g' % compare_ssim(np.abs(x_hats[ii,...]),x))

    view(x_hats)
