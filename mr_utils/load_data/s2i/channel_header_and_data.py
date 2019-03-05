'''Struct to hold both header and data for a single channel.'''

from mr_utils.load_data.s2i import sChannelHeader

class ChannelHeaderAndData(object):
    '''Struct to hold channel data.'''

    def __init__(self):
        self.header = sChannelHeader()
        # std::vector<complex_float_t> data;
        self.data = []

    def display(self):
        '''Show my contents.'''

        self.header.display()
        print('data:', len(self.data))
