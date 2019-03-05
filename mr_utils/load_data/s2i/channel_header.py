'''Holds header data for a single channel.'''

class sChannelHeader(object):
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
