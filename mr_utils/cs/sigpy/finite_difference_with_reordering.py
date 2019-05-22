'''Extend sigpy's TV recon app to include reordering.'''

import numpy as np
import sigpy as sp
from sigpy.mri.app import _estimate_weights
from sigpy.mri import linop
from sigpy.linop import Linop, Identity, Circshift, Vstack, Reshape
from sigpy import util

def FiniteDifferenceWithOrdering(ishape, axes=None, idx=None):
    '''Compute gradient of reordered signal.'''
    I = Identity(ishape)
    axes = util._normalize_axes( # pylint: disable=W0212
        axes, len(ishape))
    ndim = len(ishape)
    linops = []

    # Do the ordering
    O = Order(ishape, idx)
    R = Reshape([1] + list(ishape), ishape)
    linops.append(R*O)

    for i in range(ndim):
        D = I - Circshift(
            ishape, [0] * i + [1] + [0] * (ndim - i - 1))
        R = Reshape([1] + list(ishape), ishape)
        linops.append(R * D)

    # Do the unordering
    U = Unorder(ishape, idx)
    linops.append(R*U)

    # print(linops)
    G = Vstack(linops, axis=0)

    return G

class Order(Linop):
    '''Ordering Linop.'''
    def __init__(self, shape, idx):
        self.idx_r = idx.real.astype(int)
        self.idx_i = idx.imag.astype(int)
        self.ishape = shape
        super().__init__(shape, shape)

    def _apply(self, input): # pylint: disable=W0221,W0622
        val_r = input.real.flatten()[self.idx_r].reshape(self.ishape)
        val_i = input.imag.flatten()[self.idx_i].reshape(self.ishape)
        return val_r + 1j*val_i

    def _adjoint_linop(self):
        return self

class Unorder(Linop):
    '''Ordering Linop.'''
    def __init__(self, shape, idx):
        self.idx_r = idx.real.astype(int)
        self.idx_i = idx.imag.astype(int)
        self.ishape = shape
        super().__init__(shape, shape)

    def _apply(self, input): # pylint: disable=W0221,W0622
        val_r = np.zeros(input.size)
        val_i = np.zeros(input.size)
        val_r[self.idx_r] = input.real.flatten()[self.idx_r]
        val_i[self.idx_i] = input.imag.flatten()[self.idx_i]
        return (val_r + 1j*val_i).reshape(self.ishape)

    def _adjoint_linop(self):
        return self



class TotalVariationReconWithOrdering(sp.app.LinearLeastSquares):
    '''Modified to reorder data.'''
    def __init__(
            self, y, mps, lamda, weights=None, coord=None, idx=None,
            device=sp.cpu_device, coil_batch_size=None, comm=None,
            show_pbar=True, **kwargs):
        weights = _estimate_weights(y, weights, coord)
        if weights is not None:
            y = sp.to_device(y * weights**0.5, device=device)
        else:
            y = sp.to_device(y, device=device)

        A = linop.Sense(
            mps, coord=coord, weights=weights, comm=comm,
            coil_batch_size=coil_batch_size)

        if idx is None:
            idx = np.arange(y.size) + 1j*np.arange(y.size)

        # We need to apply reordering in the calculation of this
        # gradient
        # G = sp.linop.FiniteDifference(A.ishape)
        G = FiniteDifferenceWithOrdering(A.ishape, idx=idx)

        proxg = sp.prox.L1Reg(G.oshape, lamda)

        def g(x):
            device = sp.get_device(x)
            xp = device.xp
            with device:
                return lamda * xp.sum(xp.abs(x))

        if comm is not None:
            show_pbar = show_pbar and comm.rank == 0

        super().__init__(
            A, y, proxg=proxg, g=g, G=G, show_pbar=show_pbar,
            **kwargs)
