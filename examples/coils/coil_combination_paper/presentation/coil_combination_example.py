'''Show basic idea of coil compression.'''

from phantominator import shepp_logan
from skimage.measure import compare_nrmse

from mr_utils.coils.coil_combine import gcc
from mr_utils import view
from mr_utils.utils import sos

from examples.coils.coil_combination_paper.presentation.gaussian_csm import gaussian_csm

if __name__ == '__main__':

    # Make phantom
    N = 128
    ph = shepp_logan(N)

    # Make coils
    nc = 64
    mps = gaussian_csm(N, N, nc)
    mps += 1j*mps
    ph = ph[..., None]*mps

    view(ph, montage_axis=-1)

    for ii in [6]:
        ph_gcc = gcc(ph, vcoils=6, coil_axis=-1)
        view(ph_gcc)

        # Compare error
        ph_gcc_sos = sos(ph_gcc, axes=-1)
        ph_sos = sos(ph, axes=-1)
        print('Error:', compare_nrmse(ph_sos, ph_gcc_sos))
