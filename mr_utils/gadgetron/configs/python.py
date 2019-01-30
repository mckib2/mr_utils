'''Configs including python Gadgets.'''

from mr_utils.gadgetron import GadgetronConfig

def python():
    '''python.xml'''

    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('RemoveOversamplingPython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'remove_2x_oversampling'),
        ('python_class', 'Remove2xOversampling'),
    ])
    config.add_gadget('AccReconPython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'accumulate_and_recon'),
        ('python_class', 'AccumulateAndRecon'),
    ])
    config.add_gadget('CoilCombinePython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'rms_coil_combine'),
        ('python_class', 'RMSCoilCombine'),
    ])
    config.add_gadget('ImageViewPython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'image_viewer'),
        ('python_class', 'ImageViewer'),
    ])
    config.add_gadget('Extract')
    config.add_gadget('ImageFinish')
    return config

def python_short():
    '''python_short.xml'''

    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('RemoveOversamplingPython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'remove_2x_oversampling'),
        ('python_class', 'Remove2xOversampling'),
    ])
    config.add_gadget('AccReconPython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'accumulate_and_recon'),
        ('python_class', 'AccumulateAndRecon'),
    ])
    config.add_gadget('CoilCombinePython', 'PythonGadget', props=[
        ('python_path', '/home/myuser/scripts/python'),
        ('python_module', 'rms_coil_combine'),
        ('python_class', 'RMSCoilCombine'),
    ])
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return config
