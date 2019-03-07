'''Structure to hold the header of a scan.'''

from ctypes import c_uint16, c_uint32, c_int32, c_float

import numpy as np

from mr_utils.load_data.s2i import mdhLC, mdhCutOff, mdhSliceData

tmp = {
    'ulReserved1': c_uint32,
    'ulFlagsAndDMALength': c_uint32,
    'lMeasUID': c_int32,
    'ulScanCounter': c_uint32,
    'ulTimeStamp': c_uint32,
    'ulPMUTimeStamp': c_uint32,
    'ushSystemType': c_uint16,
    'ulPTABPosDelay': c_uint16,
    'lPTABPosX': c_int32,
    'lPTABPosY': c_int32,
    'lPTABPosZ': c_int32,
    'aulEvalInfoMask': (c_uint32, 2),
    'ushSamplesInScan': c_uint16,
    'ushUsedChannels': c_uint16,
    'sLC': mdhLC,
    'sCutOff': mdhCutOff,
    'ushKSpaceCentreColumn': c_uint16,
    'ushCoilSelect': c_uint16,
    'fReadOutOffcentre': c_float,
    'ulTimeSinceLastRF': c_uint32,
    'ushKSpaceCentreLineNo': c_uint16,
    'ushKSpaceCentrePartitionNo': c_uint16,
    'sSliceData': mdhSliceData,
    'aushIceProgramPara': (c_uint16, 24),
    'aushReservedPara': (c_uint16, 4),
    'ushApplicationCounter': c_uint16,
    'ushApplicationMask': c_uint16,
    'ulCRC': c_uint32,
}
sScanHeader = np.dtype(
    {'names': list(tmp.keys()), 'formats': list(tmp.values())})
