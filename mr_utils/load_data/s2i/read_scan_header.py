'''readScanHeader'''

import numpy as np

from mr_utils.load_data.s2i import sScanHeader, sMDH

def readScanHeader(siemens_dat, VBFILE):
    '''Read the header from the scan.'''

    # MDH and sScanHeader are incredibly similar, but sScanHeader has some
    # extra fields that we need to fill in if we only have MDH
    if VBFILE:
        scanhead = np.empty(1, dtype=sScanHeader)[0]
        mdh = np.fromfile(siemens_dat, dtype=sMDH, count=1)[0]
        scanhead['ulFlagsAndDMALength'] = mdh['ulFlagsAndDMALength']
        scanhead['lMeasUID'] = mdh['lMeasUID']
        scanhead['ulScanCounter'] = mdh['ulScanCounter']
        scanhead['ulTimeStamp'] = mdh['ulTimeStamp']
        scanhead['ulPMUTimeStamp'] = mdh['ulPMUTimeStamp']
        scanhead['ushSystemType'] = 0
        scanhead['ulPTABPosDelay'] = 0
        scanhead['lPTABPosX'] = 0
        scanhead['lPTABPosY'] = 0
        scanhead['lPTABPosZ'] = mdh['ushPTABPosNeg'] #TODO: Modify calculation
        scanhead['ulReserved1'] = 0
        scanhead['aulEvalInfoMask'] = mdh['aulEvalInfoMask'] # this is an array
        scanhead['ushSamplesInScan'] = mdh['ushSamplesInScan']
        scanhead['ushUsedChannels'] = mdh['ushUsedChannels']
        scanhead['sLC'] = mdh['sLC']
        scanhead['sCutOff'] = mdh['sCutOff']
        scanhead['ushKSpaceCentreColumn'] = mdh['ushKSpaceCentreColumn']
        scanhead['ushCoilSelect'] = mdh['ushCoilSelect']
        scanhead['fReadOutOffcentre'] = mdh['fReadOutOffcentre']
        scanhead['ulTimeSinceLastRF'] = mdh['ulTimeSinceLastRF']
        scanhead['ushKSpaceCentreLineNo'] = mdh['ushKSpaceCentreLineNo']
        scanhead['ushKSpaceCentrePartitionNo'] = mdh[
            'ushKSpaceCentrePartitionNo']
        scanhead['sSliceData'] = mdh['sSliceData']
        scanhead['aushIceProgramPara'][:8] = np.concatenate(
            (mdh['aushIceProgramPara'], mdh['aushFreePara']))
        scanhead['ushApplicationCounter'] = 0
        scanhead['ushApplicationMask'] = 0
        scanhead['ulCRC'] = 0

    else:
        scanhead = np.fromfile(siemens_dat, dtype=sScanHeader, count=1)[0]

    return(scanhead, mdh)
