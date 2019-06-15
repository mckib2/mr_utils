'''Look at 7T knee, but load from DICOM.'''

import numpy as np

from mr_utils.test_data import load_test_data
from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

if __name__ == '__main__':

    # Get the DICOMs
    path = 'mr_utils/test_data/examples/coils/7T/'

    I = np.zeros((4, 512, 512), dtype=np.complex64)
    sl = 76
    for ii in range(4):
        magfile = 'djp_trufi_%dps_25fa_LK_%d/IM-000%d-00%d.dcm' % (
            ii*90, 2*ii+9, 2*ii+1, sl)
        phasefile = 'djp_trufi_%dps_25fa_LK_%d/IM-000%d-00%d.dcm' % (
            ii*90, 2*ii+10, 2*ii+2, sl)

        print(path, magfile)

        mag, phase = load_test_data(path, [magfile, phasefile])
        # view(np.stack((mag, phase)))

        # Get arrays as floats and in the correct intervals
        mag = mag.astype(float)
        phase = phase.astype(float)
        phase /= np.max(phase.flatten())
        phase *= np.pi

        # Make complex image
        I[ii, ...] = mag*np.exp(1j*phase)
    view(I)

    lGS = gs_recon(I, pc_axis=0)
    view(lGS)
