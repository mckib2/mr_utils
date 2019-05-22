'''Reordering extension.'''

import numpy as np
import sigpy as sp
from sigpy.mri.app import _estimate_weights
from sigpy.linop import Linop
from sigpy.mri import linop
from sigpy import wavelet

class WaveletWithOrdering(Linop):
    '''Modified Wavelet linop to include reordering steps.'''

    def __init__(
            self, ishape, idx, axes=None, wave_name='db4',
            level=None):
        self.idx = idx
        self.idx_r = idx.real.astype(int)
        self.idx_i = idx.imag.astype(int)

        self.wave_name = wave_name
        self.axes = axes
        self.level = level
        oshape, _ = wavelet.get_wavelet_shape(
            ishape, wave_name, axes, level)

        super().__init__(oshape, ishape)


    def _apply(self, input): #pylint: disable=W0622

        # Apply reordering before performing wavelet transform
        sh = input.shape
        val_r = input.real.flatten()[self.idx_r].reshape(sh)
        val_i = input.imag.flatten()[self.idx_i].reshape(sh)
        input0 = val_r + 1j*val_i

        return wavelet.fwt(
            input0, wave_name=self.wave_name, axes=self.axes,
            level=self.level)

    def _adjoint_linop(self):
        return InverseWaveletWithOrdering(
            self.ishape,
            idx=self.idx,
            axes=self.axes,
            wave_name=self.wave_name,
            level=self.level)

class InverseWaveletWithOrdering(Linop):
    '''Modified inverse wavelet transform that includes unordering.'''

    def __init__(
            self, oshape, idx, axes=None, wave_name='db4',
            level=None):
        self.idx = idx
        self.idx_r = idx.real.astype(int)
        self.idx_i = idx.imag.astype(int)

        self.wave_name = wave_name
        self.axes = axes
        self.level = level
        ishape, self.coeff_slices = wavelet.get_wavelet_shape(
            oshape, wave_name, axes, level)
        super().__init__(oshape, ishape)


    def _apply(self, input): #pylint: disable=W0622

        # Do the inverse transformation
        val = wavelet.iwt(
            input, self.oshape, self.coeff_slices,
            wave_name=self.wave_name, axes=self.axes,
            level=self.level)

        # Now unorder it
        sh = val.shape
        val_r = np.zeros(val.size)
        val_i = np.zeros(val.size)
        val_r[self.idx_r] = val.real.flatten()
        val_i[self.idx_i] = val.imag.flatten()
        return (val_r + 1j*val_i).reshape(sh)

    def _adjoint_linop(self):
        return WaveletWithOrdering(
            self.oshape, self.idx, axes=self.axes,
            wave_name=self.wave_name, level=self.level)



class L1WaveletReconWithOrdering(sp.app.LinearLeastSquares):
    '''Extend L1WaveletRecon to include ordering.'''
    def __init__(
            self, y, mps, lamda, weights=None, coord=None, idx=None,
            wave_name='db4', device=sp.cpu_device,
            coil_batch_size=None, comm=None, show_pbar=True,
            **kwargs):

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

        img_shape = mps.shape[1:]
        W = WaveletWithOrdering(img_shape, idx, wave_name=wave_name)
        proxg = sp.prox.UnitaryTransform(
            sp.prox.L1Reg(W.oshape, lamda), W)

        def g(input): # pylint: disable=W0622
            device = sp.get_device(input)
            xp = device.xp
            with device:
                return lamda * xp.sum(xp.abs(W(input)))
        if comm is not None:
            show_pbar = show_pbar and comm.rank == 0

        super().__init__(
            A, y, proxg=proxg, g=g, show_pbar=show_pbar, **kwargs)
