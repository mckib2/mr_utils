'''Example EPI configurations.'''

from mr_utils.gadgetron import GadgetronConfig

def epi():
    '''Generates epi.xml.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/epi/epi.xml
    '''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('ReconX', 'EPIReconXGadget')
    config.add_gadget('EPICorr')
    config.add_gadget('FFTX', dll='gadgetron_epi')
    config.add_gadget('AccTrig', 'AcquisitionAccumulateTriggerGadget', props=[
        ('trigger_dimension', 'repetition'),
        ('sorting_dimension', 'slice')
    ])
    config.add_gadget('Buff', 'BucketToBufferGadget', props=[
        ('N_dimension', ''),
        ('S_dimension', ''),
        ('split_slices', 'true'),
        ('ignore_segment', 'true')
    ])
    config.add_gadget('FFT')
    config.add_gadget('Combine')
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return config

def epi_gtplus_grappa():
    '''GT Plus configuration file for general 2D epi reconstruction.

    Generates [1]_.

    References
    ==========
    .. [1] https://github.com/gadgetron/gadgetron/blob/master/gadgets/epi/epi_gtplus_grappa.xml
    '''

    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('NoiseAdjust')
    config.add_gadget('ReconX', 'EPIReconXGadget')
    config.add_gadget('EPICorr')
    config.add_gadget('FFTX', dll='gadgetron_epi')
    config.add_gadget('Acc', 'GtPlusAccumulatorWorkOrderTriggerGadget', props=[
        ('verboseMode', 'false'),
        ('noacceleration_triggerDim1', 'DIM_Repetition'),
        ('noacceleration_triggerDim2', 'DIM_NONE'),
        ('noacceleration_numOfKSpace_triggerDim1', '1'),
        ('separate_triggerDim1', 'DIM_Repetition'),
        ('separate_triggerDim2', 'DIM_NONE'),
        ('separate_numOfKSpace_triggerDim1', '1'),
        ('other_kspace_matching_Dim', 'DIM_Repetition')
    ])

    # Recon computation for 2DT cases
    config.add_gadget('Recon', 'GtPlusRecon2DTGadget', props=[
        # kspace data
        ('dim_4th', 'DIM_Contrast'),
        ('dim_5th', 'DIM_Slice'),

        # ork flow
        ('workOrder_ShareDim', 'DIM_Repetition'),

        # o accelaration mode
        ('no_acceleration_averageall_ref', 'true'),
        ('no_acceleration_ref_numOfModes', '0'),
        ('no_acceleration_same_combinationcoeff_allS', 'false'),
        ('no_acceleration_whichS_combinationcoeff', '0'),

        # separate mode
        ('separate_averageall_ref', 'true'),
        ('separate_ref_numOfModes', '0'),
        ('separate_fullres_coilmap', 'false'),
        ('separate_same_combinationcoeff_allS', 'false'),
        ('separate_whichS_combinationcoeff', '0'),

        # coil compression
        ('same_coil_compression_coeff_allS', 'false'),
        ('downstream_coil_compression', 'false'),
        ('coil_compression_thres', '-1'),
        ('coil_compression_num_modesKept', '-1'),

        # parameters for coil map estimation
        ('coil_map_algorithm', 'ISMRMRD_SOUHEIL'),
        ('csm_kSize', '7'),
        ('csm_powermethod_num', '3'),
        ('csm_true_3D', 'false'),
        ('csm_iter_num', '5'),
        ('csm_iter_thres', '0.001'),

        # algorithm
        ('recon_algorithm', 'ISMRMRD_GRAPPA'),
        ('recon_kspace_needed', 'false'),
        ('recon_auto_parameters', 'true'),

        # parameters for ISMRMRD_GRAPPA
        ('grappa_kSize_RO', '5'),
        ('grappa_kSize_E1', '4'),
        ('grappa_kSize_E2', '4'),
        ('grappa_reg_lamda', '0.0005'),
        ('grappa_calib_over_determine_ratio', '0'),

        # parameters for scaling and image sending
        ('min_intensity_value', '64'),
        ('max_intensity_value', '4095'),
        ('scalingFactor', '-1.0'),
        ('use_constant_scalingFactor', 'false'),

        # parameters for kspace filter, image data
        ('filterRO', 'Gaussian'),
        ('filterRO_sigma', '1.0'),
        ('filterRO_width', '0.15'),
        ('filterE1', 'Gaussian'),
        ('filterE1_sigma', '1.0'),
        ('filterE1_width', '0.15'),
        ('filterE2', 'Gaussian'),
        ('filterE2_sigma', '1.0'),
        ('filterE2_width', '0.15'),

        # parameters for kspace filter, ref data
        ('filterRefRO', 'Hanning'),
        ('filterRefRO_sigma', '1.5'),
        ('filterRefRO_width', '0.15'),
        ('filterRefE1', 'Hanning'),
        ('filterRefE1_sigma', '1.5'),
        ('filterRefE1_width', '0.15'),
        ('filterRefE2', 'Hanning'),
        ('filterRefE2_sigma', '1.5'),
        ('filterRefE2_width', '0.15'),

        # parameters for debug and timing
        ('debugFolder', ''),
        ('debugFolder2', ''),
        ('cloudNodeFile', 'myCloud_2DT.txt'),
        ('performTiming', 'true'),
        ('verboseMode', 'false'),

        # parameters for system acquisition
        ('timeStampResolution', '0.0025'),

        # parameters for recon job split
        ('job_split_by_S', 'false'),
        ('job_num_of_N', '32'),
        ('job_max_Megabytes', '10240'),
        ('job_overlap', '2'),
        ('job_perform_on_control_node', 'true')
    ])
    config.add_gadget('ComplexToFloatAttrib', 'ComplexToFloatGadget')
    config.add_gadget('FloatToShortAttrib', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')
    return config

if __name__ == '__main__':
    pass
