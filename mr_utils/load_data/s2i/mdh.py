'''All MDH related structures.'''

from ctypes import c_uint32, c_int32, c_uint16, c_float

import numpy as np

tmp = {
    'ushLine': c_uint16,
    'ushAcquisition': c_uint16,
    'ushSlice': c_uint16,
    'ushPartition': c_uint16,
    'ushEcho': c_uint16,
    'ushPhase': c_uint16,
    'ushRepetition': c_uint16,
    'ushSet': c_uint16,
    'ushSeg': c_uint16,
    'ushIda': c_uint16,
    'ushIdb': c_uint16,
    'ushIdc': c_uint16,
    'ushIdd': c_uint16,
    'ushIde': c_uint16
}
mdhLC = np.dtype({'names': list(tmp.keys()), 'formats': list(tmp.values())})

tmp = {
    'ushPre': c_uint16,
    'ushPost': c_uint16
}
mdhCutOff = np.dtype(
    {'names': list(tmp.keys()), 'formats': list(tmp.values())})

tmp = {
    'flSag': c_float,
    'flCor': c_float,
    'flTra': c_float
}
mdhSlicePosVec = np.dtype(
    {'names': list(tmp.keys()), 'formats': list(tmp.values())})

tmp = {
    'sSlicePosVec': mdhSlicePosVec,
    'aflQuaternion': (c_float, 4)
}
mdhSliceData = np.dtype(
    {'names': list(tmp.keys()), 'formats': list(tmp.values())})

tmp = {
    'ulFlagsAndDMALength': c_uint32,
    'lMeasUID': c_int32,
    'ulScanCounter': c_uint32,
    'ulTimeStamp': c_uint32,
    'ulPMUTimeStamp': c_uint32,
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
    'aushIceProgramPara': (c_uint16, 4),
    'aushFreePara': (c_uint16, 4),
    'sSliceData': mdhSliceData,
    'ushChannelId': c_uint16,
    'ushPTABPosNeg': c_uint16
}
sMDH = np.dtype({'names': list(tmp.keys()), 'formats': list(tmp.values())})
