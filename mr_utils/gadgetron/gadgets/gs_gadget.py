'''Gadgetron gadget, config file to do GS recon on each coil of GRAPPA recon.
'''

import numpy as np
# from gadgetron import Gadget
# from mr_utils.recon.ssfp import gs_recon
#
# class GS_2d(Gadget):
#
#     def process_config(self, cfg):
#         print("RMS Coil Combine, Config ignored")
#
#     def process(self, hdr, images):
#
#         # Coil dimension is last dimension of images
#         recon = gs_recon()
#
#
#         combined_image = np.sqrt(
#                np.sum(np.square(np.abs(im)),axis=(len(im.shape)-1)))
#
#         print("RMS coil", im.shape,combined_image.shape)
#         h.channels = 1
#         self.put_next(h,combined_image.astype('complex64'))
#         return 0

if __name__ == '__main__':

    from mr_utils.gadgetron import client
    from mr_utils.gadgetron import GadgetronConfig
    from mr_utils.test_data import GadgetronClient
    from mr_utils import view
    import h5py

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
        ('uncombined_channels', ','.join(str(ii) for ii in range(num_coils))),
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract', props=[
        ('extract_real', 'true'),
        ('extract_imag', 'true'),
    ])
    config.add_gadget('AutoScale')
    # config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')


    im, hdr = client(data, config_local=config.tostring(), verbose=True)
    view(im[0, ...] + 1j*im[1, ...], montage_axis=0)
