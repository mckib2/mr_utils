'''Example Gadgetron config generation.'''

from mr_utils.gadgetron import GadgetronConfig

def default():
    # pylint: disable=C0301
    '''Default config file, default.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/mri_core/config/default.xml
    '''
    # pylint: enable=C0301

    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('AccTrig', 'AcquisitionAccumulateTriggerGadget', props=[
        ('trigger_dimension', 'repetition'),
        ('sorting_dimension', 'slice')
    ])
    config.add_gadget('Buff', 'BucketToBufferGadget', props=[
        ('N_dimension', ''),
        ('S_dimension', ''),
        ('split_slices', 'true')
    ])
    config.add_gadget('SimpleRecon')
    config.add_gadget('ImageArraySplit')
    config.add_gadget('Extract')
    config.add_gadget('ImageFinish')
    return config

if __name__ == '__main__':
    pass
