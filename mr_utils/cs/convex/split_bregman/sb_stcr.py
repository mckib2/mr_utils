'''Spatially and temporally constrained Split Bregman algorithm.

Notes
-----
Adapted from [1]_.

References
----------
.. [1] https://github.com/HGGM-LIM/
       Split-Bregman-ST-Total-Variation-MRI
'''

import numpy as np
from tqdm import trange, tqdm
from skimage.measure import compare_mse

def SpatioTemporalTVSB(
        mask, y, betaxy=1, betat=1, mu=1, lam=1, gamma=None,
        nInner=1, niter=100, x=None):
    '''SpatioTemporalTVSB

    Parameters
    ----------
    mask : array_like
        undersampling matrix, same size as y
    y : array_like
        2D+time data, which corresponds to fft2(x)+noise
    betaxy : float, optional
        parameter weighting the spatial TV term (sparsiy on the
        spatial domain), use=1 and tune depending of the problem
    betat : float, optional
        parameter weighting the temporal TV term (sparsiy on the
        temporal domain), use=1 and tune depending of the problem
    mu : float, optional
        parameter weighting the data fidelity term, use mu=1
    lam : float, optional
        parameter weighting the TV constraints, use lam=1
    gamma : float, optional
        parameter to improve the conditioning, use between mu/100 and
        mu
    nInner : int, optional
        inner iterations, use n=1
    niter : int, optional
        number of (outer) iterations
    x : array_like, optional
        target image to compute the error at each iteration

    Returns
    -------
    u : array_like
        reconstructed image, size dimIm
    err : array_like, optional
        Relative solution error norm at each iteration for all
        frames.  Returned if x is provided.


    Notes
    -----
    Spatiotemporal total variation (ST-TV) using the Split Bregman
    formulation. ST-TV minimizes
       min_u |grad_x,y u|_1 + |grad_t u|_1 st. ||Fu-f||^2 < delta,
    (for more details, see the following paper)
    If you use this code, please, cite the following paper:
    P Montesinos, JFPJ Abascal, L Cuss�, J J Vaquero, M Desco.
    Application of the compressed sensing technique to self-gated
    cardiac cine sequences in small animals. Magn Reson Med., 72(2):
    369�380, 2013. DOI: http://dx.doi.org/10.1002/mrm.24936

    This code is an extension to the temporal dimension
    of spatial TV Goldstein'n code mrics.m downloaded from
    (http://www.ece.rice.edu/~tag7/Tom_Goldstein/Split_Bregman.html),
    see Tom Goldstein and Stanley Osher. The Split Bregman Method for
    L1-Regularized Problems. SIAM J. Imaging Sci., 2(2), 323�343.


    Juan Felipe P�rez-Juste Abascal, Paula Montesinos
    Departamento de Bioingenier�a e Ingenier�a Aeroespacial
    Universidad Carlos III de Madrid, Madrid, Spain
    paumsdv@gmail.com, juanabascal78@gmail.com, desco@hggm.es
    '''

    # If gamma not supplied, try mu/2
    if gamma is None:
        gamma = mu/2

    # We're expecting an image of size (rows, cols, time)
    rows, cols, numTime = mask.shape[:]

    # normalize the data so that standard parameter values work
    normFactor = getNormalizationFactor(mask[..., 0], y[..., 0])
    y *= normFactor

    # Reserve memory for the auxillary variables
    f0All = y
    u = np.zeros_like(y)
    xx = np.zeros_like(y)
    yy = np.zeros_like(y)
    bx = np.zeros_like(y)
    by = np.zeros_like(y)
    t = np.zeros_like(y)
    bt = np.zeros_like(y)

    uBest = u.copy()
    errBest = np.inf

    # RHS of the linear system
    scale = np.sqrt(rows*cols)
    murf = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(mu*y, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))*scale

    if x is not None:
        err = np.zeros((niter, numTime))
        x *= normFactor*scale
        xNorm = np.zeros(numTime)
        for it in range(numTime):
            xNorm[it] = np.linalg.norm(
                x[..., it].flatten())
        xabs = np.abs(x)


    # Build Kernels
    # Spatiotemporal Hessian in the Fourier Domain
    uker = np.zeros_like(y)
    uker[0, 0, 0] = 6
    uker[0, 1, 0] = -1
    uker[1, 0, 0] = -1
    uker[-1, 0, 0] = -1
    uker[0, -1, 0] = -1
    uker[0, 0, 1] = -1
    uker[0, 0, -1] = -1
    uker = lam*np.fft.fftn(uker) + gamma + mu*mask

    #  Do the reconstruction
    for outer in trange(niter, leave=False):
        for _inner in range(nInner):
            # update u
            # For each time
            rhs = murf + lam*(
                Dxt(xx - bx) + Dyt(yy - by) + Dtt(t - bt)) + gamma*u

            # Reconstructed image solving the equation in 3D
            u = np.fft.ifftn(np.fft.fftn(rhs)/uker)

            # update x and y
            dx = Dx(u)
            dy = Dy(u)
            dt = Dt(u)
            xx, yy = shrink2(dx + bx, dy + by, betaxy/lam)
            t = shrink1(dt + bt, betat/lam)

            # update bregman parameters
            bx += dx - xx
            by += dy - yy
            bt += dt - t

        fForw = mask*np.fft.fftshift(np.fft.fft2(np.fft.fftshift(u, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))/scale
        y += f0All - fForw
        murf = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(mu*y, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))*scale

        if x is not None:
            # Compute the error
            for it in range(numTime):
                errThis = np.linalg.norm((x[..., it] - u[
                    ..., it]).flatten())/xNorm[it]
                err[outer, it] = errThis
            curr_mse = compare_mse(xabs, np.abs(u))
            tqdm.write('MSE: %e' % curr_mse)

            if np.mean(errThis) <= errBest:
                uBest = u.copy()
                errBest = np.mean(errThis)

            # if any([outer==1 rem(outer,20)==0])
            #     figure(h); waitbar(outer/niter,h);
            #     figure(h2);
            #     imagesc(abs(u(:,:,1)));
            #     title(['ST-TV iter. ' num2str(outer) ]);
            #     colormap gray; axis image; drawnow;
            # end

    if x is not None:
        u = uBest

    # undo the normalization so that results are scaled properly
    u /= normFactor*scale

    if x is None:
        return u
    return u, err


def getNormalizationFactor(R, f):
    return 1/np.linalg.norm(f.flatten()/np.sum(R == 1).flatten())


def Dx(u):
    d = np.zeros_like(u)
    d[:, 1:, :] = u[:, 1:, :] - u[:, :-1, :]
    d[:, 0, :] = u[:, 0, :] - u[:, -1, :]
    return d

def Dxt(u):
    d = np.zeros_like(u)
    d[:, :-1, :] = u[:, :-1, :] - u[:, 1:, :]
    d[:, -1, :] = u[:, -1, :] - u[:, 0, :]
    return d

def Dy(u):
    d = np.zeros_like(u)
    d[1:, ...] = u[1:, ...] - u[:-1, ...]
    d[0, ...] = u[0, ...] - u[-1, ...]
    return d

def Dyt(u):
    d = np.zeros_like(u)
    d[:-1, ...] = u[:-1, ...] - u[1:, ...]
    d[-1, ...] = u[-1, ...] - u[0, ...]
    return d

def Dt(u):
    '''Time derivative for 3D matrix'''
    d = np.zeros_like(u)
    d[..., 1:] = u[..., 1:] - u[..., :-1]
    d[..., 0] = u[..., 0] - u[..., -1]
    return d

def Dtt(u):
    '''Time derivative for 3D matrix, transpose'''
    d = np.zeros_like(u)
    d[..., :-1] = u[..., :-1] - u[..., 1:]
    d[..., -1] = u[..., -1] - u[..., 0]
    return d

def shrink2(x, y, lam):
    s = np.sqrt(x*np.conj(x) + y*np.conj(y))
    ss = s - lam
    ss *= (ss > 0)

    s += (s < lam)
    ss /= s

    xs = ss*x
    ys = ss*y

    return xs, ys

def shrink1(x, lam):
    s = np.abs(x)
    s = np.stack((s - lam, np.zeros(s.shape)))
    return np.sign(x)*np.max(s, axis=0)
