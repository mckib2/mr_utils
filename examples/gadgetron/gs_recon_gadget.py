'''Make a Gadgetron chain that includes a python gadget.'''

import h5py

import numpy as np

from mr_utils.gadgetron import client
from mr_utils.gadgetron import GadgetronConfig
from mr_utils.test_data import GadgetronClient
from mr_utils import view

if __name__ == '__main__':

    # Load in the data
    data = GadgetronClient.grappa_input_filename()

    # Look at the data to make sure we got what we got
    with h5py.File(data, 'r') as f:
        coil_images = f['dataset']['coil_images']
        coil_images = coil_images['real'] + 1j*coil_images['imag']

        # R = 2
        tmp = np.fft.fft2(coil_images)
        tmp[..., ::2, :] = 0
        aliased = np.fft.ifft2(tmp)
        view(aliased, montage_axis=0)

    # Make the config
    num_coils = 16
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('CoilReduction', props=[
        ('coils_out', str(num_coils))
    ])
    # RO asymmetric echo handling
    config.add_gadget('AsymmetricEcho', 'AsymmetricEchoAdjustROGadget')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa', props=[
        ('target_coils', str(num_coils)),
        ('use_gpu', 'false'),
        ('uncombined_channels', ','.join(str(x) for x in range(num_coils))),
    ])
    config.add_gadget('GrappaUnmixing')
    # config.add_gadget('PassthroughPython', 'PythonGadget', props=[
    #     ('python_module', 'passthrough'),
    #     ('python_class', 'Passthrough'),
    #     ('error_ignored_mode', 'true'),
    # ])
    # config.add_gadget('GS', 'PythonGadget', props=[
    #     ('error_ignored_mode', 'true'),
    #     ('python_path', '/usr/local/share/gadgetron'),
    #     ('python_module', 'gs_recon'),
    #     ('python_class', 'ArrayImagePassThrough')
    # ])
    config.add_gadget('Extract', props=[
        ('extract_real', 'true'),
        ('extract_imag', 'true'),
    ])
    config.add_gadget('AutoScale')
    # config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')

    print(config.tostring())

    im, hdr = client(data, config_local=config.tostring(), verbose=True)
    print(im.shape)
    view(im[0, ...] + 1j*im[1, ...], montage_axis=0)
