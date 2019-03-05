'''readChannelHeaders'''

import numpy as np

from mr_utils.load_data.s2i import sMDH, ChannelHeaderAndData

def readChannelHeaders(siemens_dat, VBFILE, scanhead):
    '''Read the headers for the channels.'''

    nchannels = scanhead.ushUsedChannels
    nsamples = scanhead.ushSamplesInScan
    # channels = np.zeros((nchannels, scanhead.ushSamplesInScan))
    channels = np.empty(nchannels, dtype=object)
    for c in range(nchannels):

        if VBFILE:
            # siemens_dat.read(reinterpret_cast<char *>(&mdh), sizeof(sMDH));
            mdh = sMDH()

            if c > 0:
                mdh.ulFlagsAndDMALength = np.fromfile(
                    siemens_dat, dtype=np.uint32, count=1) #pylint: disable=E1101

                mdh.lMeasUID = np.fromfile(
                    siemens_dat, dtype=np.int32, count=1) #pylint: disable=E1101

                (mdh.ulScanCounter, mdh.ulTimeStamp,
                 mdh.ulPMUTimeStamp) = np.fromfile(
                     siemens_dat, dtype=np.uint32, count=3) #pylint: disable=E1101

                mdh.aulEvalInfoMask = np.fromfile(
                    siemens_dat, dtype=np.uint32, count=2) #pylint: disable=E1101

                mdh.ushSamplesInScan, mdh.ushUsedChannels = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101

                (mdh.sLC.ushLine, mdh.sLC.ushAcquisition, mdh.sLC.ushSlice,
                 mdh.sLC.ushPartition, mdh.sLC.ushEcho, mdh.sLC.ushPhase,
                 mdh.sLC.ushRepetition, mdh.sLC.ushSet, mdh.sLC.ushSeg,
                 mdh.sLC.ushIda, mdh.sLC.ushIdb, mdh.sLC.ushIdc,
                 mdh.sLC.ushIdd, mdh.sLC.ushIde) = np.fromfile(
                     siemens_dat, dtype=np.uint16, count=14) #pylint: disable=E1101

                mdh.sCutOff.ushPre, mdh.sCutOff.ushPost = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101

                mdh.ushKSpaceCentreColumn, mdh.ushCoilSelect = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101

                mdh.fReadOutOffcentre = np.fromfile(
                    siemens_dat, dtype=np.float32, count=1) #pylint: disable=E1101

                mdh.ulTimeSinceLastRF = np.fromfile(
                    siemens_dat, dtype=np.uint32, count=1) #pylint: disable=E1101

                (mdh.ushKSpaceCentreLineNo,
                 mdh.ushKSpaceCentrePartitionNo) = np.fromfile(
                     siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101

                mdh.aushIceProgramPara = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=4) #pylint: disable=E1101

                mdh.aushFreePara = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=4) #pylint: disable=E1101

                (mdh.sSliceData.sSlicePosVec.flSag,
                 mdh.sSliceData.sSlicePosVec.flCor,
                 mdh.sSliceData.sSlicePosVec.flTra) = np.fromfile(
                     siemens_dat, dtype=np.float32, count=3) #pylint: disable=E1101

                mdh.sSliceData.aflQuaternion = np.fromfile(
                    siemens_dat, dtype=np.float32, count=4) #pylint: disable=E1101

                mdh.ushChannelId, mdh.ushPTABPosNeg = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101

            # Now put all required fields from MDH into channel header
            channels[c] = ChannelHeaderAndData()
            channels[c].header.ulTypeAndChannelLength = 0
            channels[c].header.lMeasUID = mdh.lMeasUID
            channels[c].header.ulScanCounter = mdh.ulScanCounter
            channels[c].header.ulReserved1 = 0
            channels[c].header.ulSequenceTime = 0
            channels[c].header.ulUnused2 = 0
            channels[c].header.ulChannelId = mdh.ushChannelId
            channels[c].header.ulUnused3 = 0
            channels[c].header.ulCRC = 0

        else:
            # siemens_dat.read(reinterpret_cast<char *>(&channels[c].header),
            #     sizeof(sChannelHeader));
            raise NotImplementedError()

        channels[c].data = np.fromfile(
            siemens_dat, dtype=np.complex64, count=nsamples) #pylint: disable=E1101

    return channels
