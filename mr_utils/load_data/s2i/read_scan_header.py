'''readScanHeader'''

import numpy as np

from mr_utils.load_data.s2i import sScanHeader, sMDH

def readScanHeader(siemens_dat, VBFILE):
    '''Read the header from the scan.'''

    # Make the things we're going to fill up
    scanhead = sScanHeader()
    mdh = sMDH()

    scanhead.ulFlagsAndDMALength = np.fromfile(
        siemens_dat, dtype=np.uint32, count=1)  #pylint: disable=E1101

    # If we're VB, then we have an MDH to deal with
    if VBFILE:

        # Read everything in to the MDH skipping the first field -- you know,
        # cause we just read it up above
        # siemens_dat.read(reinterpret_cast<char *>(&mdh) + sizeof(uint32_t),
        #     sizeof(sMDH) - sizeof(uint32_t));

        mdh.lMeasUID = np.fromfile(
            siemens_dat, dtype=np.int32, count=1)

        (mdh.ulScanCounter, mdh.ulTimeStamp,
         mdh.ulPMUTimeStamp) = np.fromfile(
             siemens_dat, dtype=np.uint32, count=3) #pylint: disable=E1101

        mdh.aulEvalInfoMask = np.fromfile(
            siemens_dat, dtype=np.uint32, count=2) #pylint: disable=E1101

        mdh.ushSamplesInScan, mdh.ushUsedChannels = np.fromfile(
            siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101

        (mdh.sLC.ushLine, mdh.sLC.ushAcquisition, mdh.sLC.ushSlice,
         mdh.sLC.ushPartition, mdh.sLC.ushEcho, mdh.sLC.ushPhase,
         mdh.sLC.ushRepetition, mdh.sLC.ushSet, mdh.sLC.ushSeg, mdh.sLC.ushIda,
         mdh.sLC.ushIdb, mdh.sLC.ushIdc, mdh.sLC.ushIdd,
         mdh.sLC.ushIde) = np.fromfile(siemens_dat, dtype=np.uint16, count=14) #pylint: disable=E1101

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

        mdh.aushFreePara = np.fromfile(siemens_dat, dtype=np.uint16, count=4) #pylint: disable=E1101

        (mdh.sSliceData.sSlicePosVec.flSag,
         mdh.sSliceData.sSlicePosVec.flCor,
         mdh.sSliceData.sSlicePosVec.flTra) = np.fromfile(
             siemens_dat, dtype=np.float32, count=3) #pylint: disable=E1101

        mdh.sSliceData.aflQuaternion = np.fromfile(
            siemens_dat, dtype=np.float32, count=4) #pylint: disable=E1101

        mdh.ushChannelId, mdh.ushPTABPosNeg = np.fromfile(
            siemens_dat, dtype=np.uint16, count=2) #pylint: disable=E1101


        scanhead.lMeasUID = mdh.lMeasUID
        scanhead.ulScanCounter = mdh.ulScanCounter
        scanhead.ulTimeStamp = mdh.ulTimeStamp
        scanhead.ulPMUTimeStamp = mdh.ulPMUTimeStamp
        scanhead.ushSystemType = 0
        scanhead.ulPTABPosDelay = 0
        scanhead.lPTABPosX = 0
        scanhead.lPTABPosY = 0
        scanhead.lPTABPosZ = mdh.ushPTABPosNeg #TODO: Modify calculation
        scanhead.ulReserved1 = 0
        scanhead.aulEvalInfoMask[0] = mdh.aulEvalInfoMask[0]
        scanhead.aulEvalInfoMask[1] = mdh.aulEvalInfoMask[1]
        scanhead.ushSamplesInScan = mdh.ushSamplesInScan
        scanhead.ushUsedChannels = mdh.ushUsedChannels
        scanhead.sLC = mdh.sLC
        scanhead.sCutOff = mdh.sCutOff
        scanhead.ushKSpaceCentreColumn = mdh.ushKSpaceCentreColumn
        scanhead.ushCoilSelect = mdh.ushCoilSelect
        scanhead.fReadOutOffcentre = mdh.fReadOutOffcentre
        scanhead.ulTimeSinceLastRF = mdh.ulTimeSinceLastRF
        scanhead.ushKSpaceCentreLineNo = mdh.ushKSpaceCentreLineNo
        scanhead.ushKSpaceCentrePartitionNo = mdh.ushKSpaceCentrePartitionNo
        scanhead.sSliceData = mdh.sSliceData
        # memcpy(scanhead.aushIceProgramPara, mdh.aushIceProgramPara,
        #     8 * sizeof(uint16_t))
        scanhead.aushIceProgramPara[:8] = np.concatenate(
            (mdh.aushIceProgramPara, mdh.aushFreePara))
        scanhead.ushApplicationCounter = 0
        scanhead.ushApplicationMask = 0
        scanhead.ulCRC = 0

    else:
        # siemens_dat.read(reinterpret_cast<char*>(&scanhead)+sizeof(uint32_t),
        #                  sizeof(sScanHeader) - sizeof(uint32_t));
        raise NotImplementedError()

    return(scanhead, mdh)
