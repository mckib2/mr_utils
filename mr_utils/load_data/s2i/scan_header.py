'''Structure to hold the header of a scan.'''

import numpy as np

from mr_utils.load_data.s2i import mdhLC, mdhCutOff, mdhSliceData

class sScanHeader(object):
    '''This is the VD line header'''

    @staticmethod
    def sizeof():
        '''Get the c size of this structure.'''
        return 192

    def __init__(self):
        self.ulFlagsAndDMALength = 0
        self.lMeasUID = 0
        self.ulScanCounter = 0
        self.ulTimeStamp = 0
        self.ulPMUTimeStamp = 0
        self.ushSystemType = 0
        self.ulPTABPosDelay = 0
        self.lPTABPosX = 0
        self.lPTABPosY = 0
        self.lPTABPosZ = 0
        self.ulReserved1 = 0
        self.aulEvalInfoMask = np.zeros(2, dtype=int)
        self.ushSamplesInScan = 0
        self.ushUsedChannels = 0
        self.sLC = mdhLC()
        self.sCutOff = mdhCutOff()
        self.ushKSpaceCentreColumn = 0
        self.ushCoilSelect = 0
        self.fReadOutOffcentre = 0
        self.ulTimeSinceLastRF = 0
        self.ushKSpaceCentreLineNo = 0
        self.ushKSpaceCentrePartitionNo = 0
        self.sSliceData = mdhSliceData()
        self.aushIceProgramPara = np.zeros(24)
        self.aushReservedPara = np.zeros(4)
        self.ushApplicationCounter = 0
        self.ushApplicationMask = 0
        self.ulCRC = 0
