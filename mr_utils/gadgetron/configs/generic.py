'''Generic Gadgetron configuration files.'''

from mr_utils.gadgetron import GadgetronConfig

def generic_cartesian_grappa():
    '''Generic_Cartesian_Grappa.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/mri_core/config/Generic_Cartesian_Grappa.xml
    '''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('AsymmetricEcho', 'AsymmetricEchoAdjustROGadget')
    config.add_gadget('RemoveROOversampling')
    config.add_gadget('AccTrig', 'AcquisitionAccumulateTriggerGadget', props=[
        ('trigger_dimension', ''),
        ('sorting_dimension', '')
    ])
    config.add_gadget('BucketToBuffer', props=[
        ('N_dimension', 'contrast'),
        ('S_dimension', 'average'),
        ('split_slices', 'false'),
        ('ignore_segment', 'true'),
        ('verbose', 'true')
    ])
    config.add_gadget(
        'PrepRef', 'GenericReconCartesianReferencePrepGadget', props=[
            ('debug_folder', ''),
            ('perform_timing', 'true'),
            ('verbose', 'true'),
            ('average_all_ref_N', 'true'),
            ('average_all_ref_S', 'true'),
            ('prepare_ref_always', 'true')
        ])
    config.add_gadget(
        'CoilCompression', 'GenericReconEigenChannelGadget', props=[
            ('debug_folder', ''),
            ('perform_timing', 'true'),
            ('verbose', 'true'),
            ('average_all_ref_N', 'true'),
            ('average_all_ref_S', 'true'),
            ('upstream_coil_compression', 'true'),
            ('upstream_coil_compression_thres', '0.002'),
            ('upstream_coil_compression_num_modesKept', '0')
        ])
    config.add_gadget('Recon', 'GenericReconCartesianGrappaGadget', props=[
        ('image_series', '0'),
        ('coil_map_algorithm', 'Inati'),
        ('downstream_coil_compression', 'true'),
        ('downstream_coil_compression_thres', '0.01'),
        ('downstream_coil_compression_num_modesKept', '0'),
        ('debug_folder', ''),
        ('perform_timing', 'true'),
        ('verbose', 'true'),
        ('send_out_gfactor', 'false')
    ])
    config.add_gadget(
        'PartialFourierHandling',
        'GenericReconPartialFourierHandlingFilterGadget',
        props=[
            ('debug_folder', ''),
            ('perform_timing', 'false'),
            ('verbose', 'false'),
            ('skip_processing_meta_field', 'Skip_processing_after_recon'),
            ('partial_fourier_filter_RO_width', '0.15'),
            ('partial_fourier_filter_E1_width', '0.15'),
            ('partial_fourier_filter_E2_width', '0.15'),
            ('partial_fourier_filter_densityComp', 'false')
        ])
    config.add_gadget(
        'KSpaceFilter', 'GenericReconKSpaceFilteringGadget', props=[
            ('debug_folder', ''),
            ('perform_timing', 'false'),
            ('verbose', 'false'),
            ('skip_processing_meta_field', 'Skip_processing_after_recon'),
            ('filterRO', 'Gaussian'),
            ('filterRO_sigma', '1.0'),
            ('filterRO_width', '0.15'),
            ('filterE1', 'Gaussian'),
            ('filterE1_sigma', '1.0'),
            ('filterE1_width', '0.15'),
            ('filterE2', 'Gaussian'),
            ('filterE2_sigma', '1.0'),
            ('filterE2_width', '0.15'),
        ])
    config.add_gadget(
        'FOVAdjustment', 'GenericReconFieldOfViewAdjustmentGadget', props=[
            ('debug_folder', ''),
            ('perform_timing', 'false'),
            ('verbose', 'false')
        ])
    config.add_gadget('Scaling', 'GenericReconImageArrayScalingGadget', props=[
        ('perform_timing', 'false'),
        ('verbose', 'false'),
        ('min_intensity_value', '64'),
        ('max_intensity_value', '4095'),
        ('scalingFactor', '10.0'),
        ('use_constant_scalingFactor', 'true'),
        ('auto_scaling_only_once', 'true'),
        ('scalingFactor_dedicated', '100.0')
    ])
    config.add_gadget('ImageArraySplit')
    config.add_gadget('ComplexToFloatAttrib', 'ComplexToFloatGadget')
    config.add_gadget('FloatToShortAttrib', 'FloatToUShortGadget', props=[
        ('max_intensity', '32767'),
        ('min_intensity', '0'),
        ('intensity_offset', '0')
    ])
    config.add_gadget('ImageFinish')
    return config
