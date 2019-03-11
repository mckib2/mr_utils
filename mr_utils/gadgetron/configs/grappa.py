'''Gadgetron configs for GRAPPA gadgets.'''

from mr_utils.gadgetron import GadgetronConfig

def grappa_cpu():
    '''Generates grappa_cpu.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_cpu.xml
    '''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('PCA', 'PCACoilGadget')
    config.add_gadget('CoilReduction', props=[
        ('coils_out', '16')
    ])
    # RO asymmetric echo handling
    config.add_gadget('AsymmetricEcho', 'AsymmetricEchoAdjustROGadget')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa', props=[
        ('target_coils', '8'),
        ('use_gpu', 'false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return config

def grappa_float_cpu():
    '''Generates grappa_float_cpu.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_float_cpu.xml
    '''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('PCA', 'PCACoilGadget')
    config.add_gadget('CoilReduction', props=[
        ('coils_out', '16')
    ])
    # RO asymmetric echo handling
    config.add_gadget('AsymmetricEcho', 'AsymmetricEchoAdjustROGadget')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa', props=[
        ('target_coils', '8'),
        ('use_gpu', 'false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('ImageFinish')
    return config

def grappa_unoptimized_cpu():
    '''Generates grappa_unoptimized_cpu.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_unoptimized.xml
    '''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa', props=[
        ('target_coils', '8'),
        ('use_gpu', 'false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return config

def grappa_unoptimized_float_cpu():
    '''Generates grappa_unoptimized_float_cpu.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_unoptimized_float.xml
    '''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa', props=[
        ('target_coils', '8'),
        ('use_gpu', 'false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('ImageFinish')
    return config

if __name__ == '__main__':
    pass
