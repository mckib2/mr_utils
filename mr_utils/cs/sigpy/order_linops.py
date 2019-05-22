'''Classes to apply ordering and inverse ordering as linops for sigpy.
'''

import numpy as np
from sigpy.linop import Linop

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
