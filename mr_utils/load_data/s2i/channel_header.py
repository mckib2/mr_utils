'''Holds header data for a single channel.'''

from ctypes import c_uint16, c_uint32, c_int32

import numpy as np

tmp = {
    'ulTypeAndChannelLength': c_uint32,
    'lMeasUID': c_int32,
    'ulScanCounter': c_uint32,
    'ulReserved1': c_uint32,
    'ulSequenceTime': c_uint32,
    'ulUnused2': c_uint32,
    'ulChannelId': c_uint16,
    'ulUnused3': c_uint16,
    'ulCRC': c_uint32
}
sChannelHeader = np.dtype(
    {'names': list(tmp.keys()), 'formats': list(tmp.values())})

class sChannelHeader_old(object):
    '''Struct to hold channel header data.'''

    @staticmethod
    def sizeof():
        '''Returns c size of struct.'''
        return 32

    def __init__(self):
        self.ulTypeAndChannelLength = 0
        self.lMeasUID = 0
        self.ulScanCounter = 0
        self.ulReserved1 = 0
        self.ulSequenceTime = 0
        self.ulUnused2 = 0
        self.ulChannelId = 0
        self.ulUnused3 = 0
        self.ulCRC = 0

    def display(self):
        '''Show my innards.'''

        print('tsChannelHeader:')
        print('\tsChannelHeader.ulTypeAndChannelLength',
              self.ulTypeAndChannelLength)
        print('\tsChannelHeader.lMeasUID', self.lMeasUID)
        print('\tsChannelHeader.ulScanCounter', self.ulScanCounter)
        print('\tsChannelHeader.ulReserved1', self.ulReserved1)
        print('\tsChannelHeader.ulSequenceTime', self.ulSequenceTime)
        print('\tsChannelHeader.ulUnused2', self.ulUnused2)
        print('\tsChannelHeader.ulChannelId', self.ulChannelId)
        print('\tsChannelHeader.ulUnused3', self.ulUnused3)
        print('\tsChannelHeader.ulCRC', self.ulCRC)
