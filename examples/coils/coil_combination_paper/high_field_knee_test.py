'''Try running 7T data.'''

import numpy as np

from mr_utils.test_data import load_test_data
from mr_utils.definitions import ROOT_DIR
from mr_utils.gadgetron import client, GadgetronConfig
from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

if __name__ == '__main__':

    path = 'mr_utils/test_data/examples/coils/'
    # filename = 'knee_bssfp_7t.npy'
    filename = 'meas_MID203_djp_trufi_0ps_25fa_LK_FID49221.dat'
    # filename = 'knee_bssfp_7t_pc0.h5'
    load_test_data(path, [filename], do_return=False) # too big
    datafile = '%s/%s' % (path, filename)

    # # This is undersampled R=2, so we need to do GRAPPA
    # data, hdr = client(datafile, config='grappa.xml')
    # view(data)

    num_coils = 28
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('CoilReduction', props=[
        ('coils_out', str(num_coils))
    ])
    # RO asymmetric echo handling
    config.add_gadget(
        'AsymmetricEcho', 'AsymmetricEchoAdjustROGadget')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa', props=[
        ('target_coils', str(num_coils)),
        ('use_gpu', 'false'),
        ('uncombined_channels',
         ','.join(str(x) for x in range(num_coils))),
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract', props=[
        ('extract_real', 'true'),
        ('extract_imag', 'true'),
    ])
    config.add_gadget('AutoScale')
    config.add_gadget('ImageFinish')

    print(config.tostring())

    # Currently I think I'm running out of memory, so I'll have to try
    # this on POGO.
    data, hdr = client(
        datafile, config_local=config.tostring(), verbose=True)
    print(data.shape)

    # pcs = np.memmap(
    #     fullpath, dtype=np.complex64, mode='r',
    #     shape=(4, 384, 384, 40, 28))
    #
    #
    # ax = (1, 2)
    # pcs0 = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(
    #     pcs[..., 10, 0], axes=ax), axes=ax), axes=ax)
    # recon = gs_recon(pcs0, pc_axis=0)
    # view(recon)
