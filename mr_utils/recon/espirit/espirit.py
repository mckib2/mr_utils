## Adapted from https://github.com/peng-cao/mripy

import numpy as np
import scipy
import scipy.signal as ss

def hamming2d( a, b ):
    # build 2d window
    w2d = np.outer(ss.hamming(a), ss.hamming(b))
    return np.sqrt(w2d)

# the first half dimentions are window dimentions,
# the second half dimentions are rolling/repeating dimentions
def hankelnd_r( a, win_shape, win_strides = None ):
    if win_strides is None:
        win_strides = np.ones(win_shape.__len__()).astype(int)

    win_shape = np.array(win_shape)
    win_strides = np.array(win_strides)
    #print win_strides,win_shape,a.shape

    #get size and shape
    a_shape = np.array(a.shape)
    a_strides = np.array(a.strides)
    #define shape of block hankel matrix, half is num_movements of hankel matrix, half is num_movements inside window
    bh_shape = np.concatenate((win_shape, np.divide(a_shape - win_shape, win_strides).astype(int) + 1))
    #define each move/strides in a hankel window, match bh_shape
    # half is strides of hankel matrix, half is strides of movements inside window
    bh_strides = np.concatenate((a_strides, np.multiply(win_strides,a_strides)))

    return np.lib.stride_tricks.as_strided(a, shape=bh_shape, strides=bh_strides)


def pad2d( data, nx, ny ):
    '''
    zero pad the 2d k-space in kx and ky dimentions
    '''

    #create undersampling mask
    datsize    = data.shape
    padsize    = np.array(datsize)
    padsize[0] = nx
    padsize[1] = ny
    ndata = np.zeros(tuple(padsize),dtype = data.dtype)

    # center k-space index range
    datrx = np.int(datsize[0]/2)
    datry = np.int(datsize[1]/2)
    cx = np.int(nx/2)
    cy = np.int(ny/2)
    cxr = np.arange(round(cx-datrx),round(cx-datrx+datsize[0]))
    cyr = np.arange(round(cy-datry),round(cy-datry+datsize[1]))
    # print(cxr,cyr)
    # print(map(int,cxr))
    ndata[np.ix_(list(map(int,cxr)),list(map(int,cyr)))] = data
    return ndata

class FFT2d:
    '''
    these classes apply  FFT for the input image,
     and some also apply mask in the forward function
    the order is
    k-space -> image for forward;
    image -> k-space is backward

    this is 2d FFT without k-space mask for CS MRI recon
    '''

    def __init__( self, axes = (0,1)):
        #self.mask = mask #save the k-space mask
        self.axes = axes
    # let's call k-space <- image as forward
    def forward( self, im ):
        im = np.fft.fftshift(im,self.axes)
        ksp = np.fft.fft2(im,s=None,axes=self.axes)
        ksp = np.fft.ifftshift(ksp,self.axes)
        return ksp

    # let's call image <- k-space as backward
    def backward( self, ksp ):
        ksp = np.fft.fftshift(ksp,self.axes)
        #im = np.fft.ifft2(ksp,s=None,axes=(0,1))#noted that numpy.fft by default applies to last two dims
        im = np.fft.ifft2(ksp,s=None,axes=self.axes)
        im = np.fft.ifftshift(im,self.axes)
        return im

def espirit_2d(
        xcrop,
        x_shape,
        nsingularv=150,
        hkwin_shape=(16,16),
        pad_before_espirit=0,
        pad_fact=1,
        sigv_th=0.01,
        nsigv_th=0.2):
    '''
    2d espirit

    Inputs
    xcrop is 3d matrix with first two dimentions as nx,ny and third one as coil
    nsingularv = 150, number of truncated singular vectors

    outputs
    Vim the sensitivity map
    sim the singular value map
    '''

    ft = FFT2d()#2d fft operator
    # ft = FFTW2d()#2d fft operator
    #timing = utc.timing()
    #multidimention tensor as the block hankel matrix
    #first 2 are x, y dims with rolling window size of hkwin_shape
    #last 1 is coil dimension, with stride of 1
    #timing.start()
    h = hankelnd_r(xcrop, (hkwin_shape[0], hkwin_shape[1], 1))
    #timing.stop().display('Create Hankel ').start()
    dimh = h.shape
    #flatten the tensor to create a matrix= [flatten(fist3 dims), flatten(last3 dims)]
    #the second dim of hmtx contain coil information, i.e. dimh[2]=1, dimh[5]=N_coils
    hmtx = h.reshape(( dimh[0]* dimh[1]* dimh[2], dimh[3], dimh[4], dimh[5])).\
             reshape(( dimh[0]* dimh[1]* dimh[2], dimh[3]* dimh[4]* dimh[5]))
    #timing.stop().display('Reshape Hankel ').start()
    #svd, could try other approaches
    # V has the coil information since the second dim of hmtx has coil data
    U, s, V = np.linalg.svd(hmtx, full_matrices=False)
    #U, s, V = scipy.sparse.linalg.svds(hmtx, nsingularv )
    #U, s, V = scipy.sparse.linalg.svds(hmtx, nsingularv )
    #timing.stop().display('SVD ')
    for k in range(len(s)):
        # if s[k] > s[0]*nsing_th:
        if s[k] > s[0]*nsigv_th:
            nsingularv = k
    print('exctract %g out of %g singular vectors:' % (nsingularv, len(s)))
    #S = np.diag(s)
    #ut.plotim1(np.absolute(V[:,0:150]).T)#plot V singular vectors
    #ut.plot(s)#plot singular values
    #invh = np.zeros(x.shape,complex)
    #print h.shape
    #hk.invhankelnd(h,invh,(2,3,1))

    #reshape vn to generate k-space vn tensor
    vn = V[0:nsingularv,:].reshape((nsingularv,dimh[3],dimh[4],dimh[5])).transpose((1,2,0,3))

    #zero pad vn, vn matrix of reshaped singular vectors,
    #dims of vn: nx,ny,nsingularv,ncoil
    #nx = x_shape[0]
    #ny = x_shape[1]
    # do pading before espirit
    if pad_before_espirit is 0:
        nx = min(pad_fact * xcrop.shape[0], x_shape[0])
        ny = min(pad_fact * xcrop.shape[1], x_shape[1])
    else:
        nx = x_shape[0]
        ny = x_shape[1]
    # coil dim
    nc   = x_shape[2]
    # filter
    hwin = hamming2d(vn.shape[0],vn.shape[1])
    # apply hamming window
    vn   = np.multiply(vn, hwin[:,:,np.newaxis,np.newaxis])
    vn   = pad2d(vn,nx,ny)
    #plot first singular vecctor Vn[0]
    imvn = ft.backward(vn)
    #ut.plotim3(np.absolute(imvn[:,:,0,:].squeeze()))#spatial feature of V[:,1] singular vector
    sim  = np.zeros((nx,ny), dtype = np.complex128)
    Vim  = np.zeros((nx,ny,nc), dtype = np.complex128)
    for ix in range(nx):
        for iy in range(ny):
            vpix         = imvn[ix,iy,:,:].squeeze()
            vpix         = np.matrix(vpix).transpose()
            vvH          = vpix.dot(vpix.getH())
            U, s, V      = np.linalg.svd(vvH, full_matrices=False)
            sim[ix,iy]   = s[0]
            Vim[ix,iy,:] = V[0,:].squeeze()


    Vim = np.conj(Vim)
    if pad_before_espirit is 0:
        Vim = ft.backward(pad2d(ft.forward(Vim),x_shape[0],x_shape[1]))
        sim = ft.backward(pad2d(ft.forward(sim),x_shape[0],x_shape[1]))
    #plot first eigen vector, eigen value
    #ut.plotim3(np.absolute(Vim))
    #ut.plotim1(np.absolute(sim))
    #Vim_dims_name = ['x', 'y', 'coil']
    #sim_dims_name = ['x', 'y']
    Vimnorm = np.linalg.norm(Vim, axis = 2)
    Vim = np.divide(Vim, 1e-6 + Vimnorm[:,:,np.newaxis])
    sim = sim/np.max(sim.flatten())
    for ix in range(x_shape[0]):
        for iy in range(x_shape[1]):
                if sim[ix,iy] < sigv_th:
                    Vim[ix,iy,:] = np.zeros(nc)
    return Vim, np.absolute(sim) #, Vim_dims_name, sim_dims_name
