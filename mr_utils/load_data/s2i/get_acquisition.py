'''Populate ISMRMRD Acquisition object with data from ChannelHeaderAndData.
'''

import warnings
import logging

import numpy as np
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=FutureWarning)
    from ismrmrd import Acquisition

from mr_utils.load_data.s2i import defs

def getAcquisition(flash_pat_ref_scan, trajectory, dwell_time_0, max_channels,
                   _isAdjustCoilSens, _isAdjQuietCoilSens, _isVB, traj,
                   scanhead, channels):
    '''Create ISMRMRD acqusition object for the current channel data.'''

    ismrmrd_acq = Acquisition()
    # The number of samples, channels and trajectory dimensions is set below

    # Acquisition header values are zero by default
    ismrmrd_acq.measurement_uid = scanhead['lMeasUID']
    ismrmrd_acq.scan_counter = scanhead['ulScanCounter']
    ismrmrd_acq.acquisition_time_stamp = scanhead['ulTimeStamp']
    ismrmrd_acq.physiology_time_stamp[0] = scanhead['ulPMUTimeStamp'] #pylint: disable=E1101
    ismrmrd_acq.available_channels = max_channels
    # Mask to indicate which channels are active. Support for 1024 channels
    # uint64_t channel_mask[16];
    ismrmrd_acq.discard_pre = scanhead['sCutOff']['ushPre']
    ismrmrd_acq.discard_post = scanhead['sCutOff']['ushPost']
    ismrmrd_acq.center_sample = scanhead['ushKSpaceCentreColumn']

    # std::cout << "isAdjustCoilSens, isVB : " << isAdjustCoilSens << " "
    #           << isVB << std::endl;

    # Is this is noise?
    if scanhead['aulEvalInfoMask'][0] & (1 << 25):
        raise NotImplementedError()
        # ismrmrd_acq.sample_time_us() = compute_noise_sample_in_us(
        #     scanhead.ushSamplesInScan, isAdjustCoilSens, isAdjQuietCoilSens,
        #     isVB)
    else:
        ismrmrd_acq.sample_time_us = dwell_time_0 / 1000.0

    # std::cout << "ismrmrd_acq.sample_time_us(): "
    #           << ismrmrd_acq.sample_time_us() << std::endl;

    ismrmrd_acq.position[0] = scanhead['sSliceData']['sSlicePosVec']['flSag'] #pylint: disable=E1101
    ismrmrd_acq.position[1] = scanhead['sSliceData']['sSlicePosVec']['flCor'] #pylint: disable=E1101
    ismrmrd_acq.position[2] = scanhead['sSliceData']['sSlicePosVec']['flTra'] #pylint: disable=E1101

    # Convert Siemens quaternions to direction cosines.
    # In the Siemens convention the quaternion corresponds to a rotation
    # matrix with columns P R S
    # Siemens stores the quaternion as (W,X,Y,Z)
    quat = np.zeros(4)
    quat[0] = scanhead['sSliceData']['aflQuaternion'][1] # X
    quat[1] = scanhead['sSliceData']['aflQuaternion'][2] # Y
    quat[2] = scanhead['sSliceData']['aflQuaternion'][3] # Z
    quat[3] = scanhead['sSliceData']['aflQuaternion'][0] # W
    # ISMRMRD::ismrmrd_quaternion_to_directions(quat,
    #                                           ismrmrd_acq.phase_dir(),
    #                                           ismrmrd_acq.read_dir(),
    #                                           ismrmrd_acq.slice_dir());


    ismrmrd_acq.patient_table_position[0] = scanhead['lPTABPosX'] #pylint: disable=E1101
    ismrmrd_acq.patient_table_position[1] = scanhead['lPTABPosY'] #pylint: disable=E1101
    ismrmrd_acq.patient_table_position[2] = scanhead['lPTABPosZ'] #pylint: disable=E1101

    # This doesn't seem to get used...
    # fixedE1E2 = True
    # if scanhead.aulEvalInfoMask[0] & (1 << 25):
    #     fixedE1E2 = False # noise
    # if scanhead.aulEvalInfoMask[0] & (1 << 1):
    #     fixedE1E2 = False # navigator, rt feedback
    # if scanhead.aulEvalInfoMask[0] & (1 << 2):
    #     fixedE1E2 = False # hp feedback
    # if scanhead.aulEvalInfoMask[0] & (1 << 51):
    #     fixedE1E2 = False # dummy
    # if scanhead.aulEvalInfoMask[0] & (1 << 5):
    #     fixedE1E2 = False # synch data

    ismrmrd_acq.idx.average = scanhead['sLC']['ushAcquisition'] #pylint: disable=E1101
    ismrmrd_acq.idx.contrast = scanhead['sLC']['ushEcho'] #pylint: disable=E1101
    ismrmrd_acq.idx.kspace_encode_step_1 = scanhead['sLC']['ushLine'] #pylint: disable=E1101
    ismrmrd_acq.idx.kspace_encode_step_2 = scanhead['sLC']['ushPartition'] #pylint: disable=E1101
    ismrmrd_acq.idx.phase = scanhead['sLC']['ushPhase'] #pylint: disable=E1101
    ismrmrd_acq.idx.repetition = scanhead['sLC']['ushRepetition'] #pylint: disable=E1101
    ismrmrd_acq.idx.segment = scanhead['sLC']['ushSeg'] #pylint: disable=E1101
    ismrmrd_acq.idx.set = scanhead['sLC']['ushSet'] #pylint: disable=E1101
    ismrmrd_acq.idx.slice = scanhead['sLC']['ushSlice'] #pylint: disable=E1101
    ismrmrd_acq.idx.user[0] = scanhead['sLC']['ushIda'] #pylint: disable=E1101
    ismrmrd_acq.idx.user[1] = scanhead['sLC']['ushIdb'] #pylint: disable=E1101
    ismrmrd_acq.idx.user[2] = scanhead['sLC']['ushIdc'] #pylint: disable=E1101
    ismrmrd_acq.idx.user[3] = scanhead['sLC']['ushIdd'] #pylint: disable=E1101
    ismrmrd_acq.idx.user[4] = scanhead['sLC']['ushIde'] #pylint: disable=E1101
    # TODO: remove this once the GTPlus can properly autodetect partial fourier
    ismrmrd_acq.idx.user[5] = scanhead['ushKSpaceCentreLineNo'] #pylint: disable=E1101
    ismrmrd_acq.idx.user[6] = scanhead['ushKSpaceCentrePartitionNo'] #pylint: disable=E1101

    # *************************************************************************
    # the user_int[0] and user_int[1] are used to store user defined parameters
    # *************************************************************************
    ismrmrd_acq.user_int[0] = int(scanhead['aushIceProgramPara'][0]) #pylint: disable=E1101
    ismrmrd_acq.user_int[1] = int(scanhead['aushIceProgramPara'][1]) #pylint: disable=E1101
    ismrmrd_acq.user_int[2] = int(scanhead['aushIceProgramPara'][2]) #pylint: disable=E1101
    ismrmrd_acq.user_int[3] = int(scanhead['aushIceProgramPara'][3]) #pylint: disable=E1101
    ismrmrd_acq.user_int[4] = int(scanhead['aushIceProgramPara'][4]) #pylint: disable=E1101
    ismrmrd_acq.user_int[5] = int(scanhead['aushIceProgramPara'][5]) #pylint: disable=E1101
    ismrmrd_acq.user_int[6] = int(scanhead['aushIceProgramPara'][6]) #pylint: disable=E1101
    # TODO: in the newer version of ismrmrd, add field to store
    # time_since_perp_pulse
    ismrmrd_acq.user_int[7] = int(scanhead['ulTimeSinceLastRF']) #pylint: disable=E1101

    ismrmrd_acq.user_float[0] = float(scanhead['aushIceProgramPara'][8]) #pylint: disable=E1101
    ismrmrd_acq.user_float[1] = float(scanhead['aushIceProgramPara'][9]) #pylint: disable=E1101
    ismrmrd_acq.user_float[2] = float(scanhead['aushIceProgramPara'][10]) #pylint: disable=E1101
    ismrmrd_acq.user_float[3] = float(scanhead['aushIceProgramPara'][11]) #pylint: disable=E1101
    ismrmrd_acq.user_float[4] = float(scanhead['aushIceProgramPara'][12]) #pylint: disable=E1101
    ismrmrd_acq.user_float[5] = float(scanhead['aushIceProgramPara'][13]) #pylint: disable=E1101
    ismrmrd_acq.user_float[6] = float(scanhead['aushIceProgramPara'][14]) #pylint: disable=E1101
    ismrmrd_acq.user_float[7] = float(scanhead['aushIceProgramPara'][15]) #pylint: disable=E1101

    if scanhead['aulEvalInfoMask'][0] & (1 << 25):
        ismrmrd_acq.setFlag(defs.ACQ_IS_NOISE_MEASUREMENT)
    if scanhead['aulEvalInfoMask'][0] & (1 << 28):
        ismrmrd_acq.setFlag(defs.ACQ_FIRST_IN_SLICE)
    if scanhead['aulEvalInfoMask'][0] & (1 << 29):
        ismrmrd_acq.setFlag(defs.ACQ_LAST_IN_SLICE)
    if scanhead['aulEvalInfoMask'][0] & (1 << 11):
        ismrmrd_acq.setFlag(defs.ACQ_LAST_IN_REPETITION)

    # if a line is both image and ref, then do not set the ref flag
    if scanhead['aulEvalInfoMask'][0] & (1 << 23):
        ismrmrd_acq.setFlag(defs.ACQ_IS_PARALLEL_CALIBRATION_AND_IMAGING)
    else:
        if scanhead['aulEvalInfoMask'][0] & (1 << 22):
            ismrmrd_acq.setFlag(defs.ACQ_IS_PARALLEL_CALIBRATION)


    if scanhead['aulEvalInfoMask'][0] & (1 << 24):
        ismrmrd_acq.setFlag(defs.ACQ_IS_REVERSE)
    if scanhead['aulEvalInfoMask'][0] & (1 << 11):
        ismrmrd_acq.setFlag(defs.ACQ_LAST_IN_MEASUREMENT)
    if scanhead['aulEvalInfoMask'][0] & (1 << 21):
        ismrmrd_acq.setFlag(defs.ACQ_IS_PHASECORR_DATA)
    if scanhead['aulEvalInfoMask'][0] & (1 << 1):
        ismrmrd_acq.setFlag(defs.ACQ_IS_NAVIGATION_DATA)
    if scanhead['aulEvalInfoMask'][0] & (1 << 1):
        ismrmrd_acq.setFlag(defs.ACQ_IS_RTFEEDBACK_DATA)
    if scanhead['aulEvalInfoMask'][0] & (1 << 2):
        ismrmrd_acq.setFlag(defs.ACQ_IS_HPFEEDBACK_DATA)
    if scanhead['aulEvalInfoMask'][0] & (1 << 51):
        ismrmrd_acq.setFlag(defs.ACQ_IS_DUMMYSCAN_DATA)
    if scanhead['aulEvalInfoMask'][0] & (1 << 10):
        ismrmrd_acq.setFlag(defs.ACQ_IS_SURFACECOILCORRECTIONSCAN_DATA)
    if scanhead['aulEvalInfoMask'][0] & (1 << 5):
        ismrmrd_acq.setFlag(defs.ACQ_IS_DUMMYSCAN_DATA)
    # if scanhead.aulEvalInfoMask[0] & (1ULL << 1):
    #     ismrmrd_acq.setFlag(ISMRMRD_ACQ_LAST_IN_REPETITION)

    if scanhead['aulEvalInfoMask'][0] & (1 << 46):
        ismrmrd_acq.setFlag(defs.ACQ_LAST_IN_MEASUREMENT)

    if flash_pat_ref_scan and ismrmrd_acq.isFlagSet(
            defs.ACQ_IS_PARALLEL_CALIBRATION):
        # For some sequences the PAT Reference data is collected using
        # a different encoding space, e.g. EPI scans with FLASH PAT Reference
        # enabled by command line option
        # TODO: it is likely that the dwell time is not set properly for this
        # type of acquisition
        ismrmrd_acq.encoding_space_ref = 1

    # Spiral and not noise, we will add the trajectory to the data
    if trajectory == 'TRAJECTORY_SPIRAL' and not ismrmrd_acq.isFlagSet(
            defs.ACQ_IS_NOISE_MEASUREMENT):


        # from above we have the following
        # traj_dim[0] = dimensionality (2)
        # traj_dim[1] = ngrad i.e. points per interleaf
        # traj_dim[2] = no. of interleaves
        # and
        # traj.getData() is a float * pointer to the trajectory stored
        # kspace_encode_step_1 is the interleaf number

        # Set the acquisition number of samples, channels and trajectory
        # dimensions this reallocates the memory
        traj_dim = traj.getDims()
        ismrmrd_acq.resize(
            scanhead['ushSamplesInScan'], scanhead['ushUsedChannels'],
            traj_dim[0])

        traj_samples_to_copy = ismrmrd_acq.number_of_samples() #pylint: disable=E1101
        if traj_dim[1] < traj_samples_to_copy:
            traj_samples_to_copy = traj_dim[1]
            ismrmrd_acq.discard_post = \
                ismrmrd_acq.number_of_samples() - traj_samples_to_copy #pylint: disable=E1101

        # NEED TO DO THESE LINES:
        # float *t_ptr = &traj.getDataPtr()[traj_dim[0] * traj_dim[1]
        # * ismrmrd_acq.idx().kspace_encode_step_1];
        # memcpy((void *) ismrmrd_acq.getTrajPtr(), t_ptr, sizeof(float)
        # * traj_dim[0] * traj_samples_to_copy);
        raise NotImplementedError()
    else: # No trajectory
        # Set the acquisition number of samples, channels and trajectory
        # dimensions; this reallocates the memory
        ismrmrd_acq.resize(
            scanhead['ushSamplesInScan'], scanhead['ushUsedChannels'])

    for c in range(ismrmrd_acq.active_channels): #pylint: disable=E1101
        ismrmrd_acq.data[:] = channels[c].data
        # memcpy((complex_float_t *) &(ismrmrd_acq.getDataPtr()[c
        #  ismrmrd_acq.number_of_samples()]),
        #        &channels[c].data[0], ismrmrd_acq.number_of_samples()
        # * sizeof(complex_float_t))


    if np.mod(scanhead['ulScanCounter'], 1000) == 0:
        logging.info('wrote scan: %d', scanhead['ulScanCounter'])

    return ismrmrd_acq
