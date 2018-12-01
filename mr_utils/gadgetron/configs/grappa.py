from mr_utils.gadgetron import GadgetronConfig

def grappa_cpu():
    config = GadgetronConfig()
    config.add_reader('1008','GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026','GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022','MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('PCA','PCACoilGadget')
    config.add_gadget('CoilReduction',props=[
        ('coils_out','16')
    ])
    config.add_gadget('AsymmetricEcho','AsymmetricEchoAdjustROGadget') # RO asymmetric echo handling
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa',props=[
        ('target_coils','8'),
        ('use_gpu','false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort','FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return(config)

def grappa_float_cpu():
    config = GadgetronConfig()
    config.add_reader('1008','GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026','GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022','MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('PCA','PCACoilGadget')
    config.add_gadget('CoilReduction',props=[
        ('coils_out','16')
    ])
    config.add_gadget('AsymmetricEcho','AsymmetricEchoAdjustROGadget') # RO asymmetric echo handling
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa',props=[
        ('target_coils','8'),
        ('use_gpu','false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('ImageFinish')
    return(config)

def grappa_unoptimized_cpu():
    config = GadgetronConfig()
    config.add_reader('1008','GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026','GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022','MRIImageWriter')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa',props=[
        ('target_coils','8'),
        ('use_gpu','false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort','FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return(config)

def grappa_unoptimized_float_cpu():
    config = GadgetronConfig()
    config.add_reader('1008','GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026','GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022','MRIImageWriter')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('Grappa',props=[
        ('target_coils','8'),
        ('use_gpu','false')
    ])
    config.add_gadget('GrappaUnmixing')
    config.add_gadget('Extract')
    config.add_gadget('ImageFinish')
    return(config)

if __name__ == '__main__':
    pass
