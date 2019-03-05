'''All MDH related structures.'''

import numpy as np

class mdhLC(object):
    '''Filler.'''
    def __init__(self):
        self.ushLine = 0
        self.ushAcquisition = 0
        self.ushSlice = 0
        self.ushPartition = 0
        self.ushEcho = 0
        self.ushPhase = 0
        self.ushRepetition = 0
        self.ushSet = 0
        self.ushSeg = 0
        self.ushIda = 0
        self.ushIdb = 0
        self.ushIdc = 0
        self.ushIdd = 0
        self.ushIde = 0

class mdhCutOff(object):
    '''Filler.'''
    def __init__(self):
        self.ushPre = 0
        self.ushPost = 0

class mdhSlicePosVec(object):
    '''Filler.'''
    def __init__(self):
        self.flCor = 0
        self.flSag = 0
        self.flTra = 0

class mdhSliceData(object):
    '''Filler.'''
    def __init__(self):
        self.sSlicePosVec = mdhSlicePosVec()
        self.aflQuaternion = np.zeros(4)

class sMDH(object):
    '''This is the VB line header'''

    @staticmethod
    def sizeof():
        '''Get the c size of this structure.'''
        return 128

    def __init__(self):
        self.ulFlagsAndDMALength = 0
        self.lMeasUID = 0
        self.ulScanCounter = 0
        self.ulTimeStamp = 0
        self.ulPMUTimeStamp = 0
        self.aulEvalInfoMask = np.zeros(2, dtype=int)
        self.ushSamplesInScan = 0
        self.ushUsedChannels = 0
        self.sLC = mdhLC()
        self.sCutOff = mdhCutOff()

        self.ushKSpaceCentreColumn = 0
        self.ushCoilSelect = 0
        self.fReadOutOffcentre = 0.0
        self.ulTimeSinceLastRF = 0
        self.ushKSpaceCentreLineNo = 0
        self.ushKSpaceCentrePartitionNo = 0
        self.aushIceProgramPara = np.zeros(24, dtype=int)
        self.aushFreePara = np.zeros(4, dtype=int)

        self.sSliceData = mdhSliceData()

        self.ushChannelId = 0
        self.ushPTABPosNeg = 0

    def display(self):
        '''Give a look into your soul.'''

        print('MDH:')
        print('\tmdh.ulFlagsAndDMALength', self.ulFlagsAndDMALength)
        print('\tmdh.lMeasUID', self.lMeasUID)

        print('\tmdh.ulScanCounter', self.ulScanCounter)

        print('\tmdh.ulTimeStamp', self.ulTimeStamp)

        print('\tmdh.ulPMUTimeStamp', self.ulPMUTimeStamp)
        print('\tmdh.aulEvalInfoMask', self.aulEvalInfoMask)
        print('\tmdh.ushSamplesInScan', self.ushSamplesInScan)
        print('\tmdh.ushUsedChannels', self.ushUsedChannels)

        print('\tmdh.sLC', self.sLC)
        print('\tmdh.sCutOff', self.sCutOff)
        print('\tmdh.ushKSpaceCentreColumn', self.ushKSpaceCentreColumn)
        print('\tmdh.ushCoilSelect', self.ushCoilSelect)

        print('\tmdh.fReadOutOffcentre', self.fReadOutOffcentre)
        print('\tmdh.ulTimeSinceLastRF', self.ulTimeSinceLastRF)
        print('\tmdh.ushKSpaceCentreLineNo', self.ushKSpaceCentreLineNo)
        print('\tmdh.ushKSpaceCentrePartitionNo',
              self.ushKSpaceCentrePartitionNo)
        print('\tmdh.aushIceProgramPara', self.aushIceProgramPara)
        print('\tmdh.aushFreePara', self.aushFreePara)
        print('\tmdh.sSliceData', self.sSliceData)
        print('\tmdh.ushChannelId', self.ushChannelId)

        print('\tmdh.ushPTABPosNeg', self.ushPTABPosNeg)
