'''Struct to hold both header and data for a single channel.'''

import numpy as np

from mr_utils.load_data.s2i import sChannelHeader

class ChannelHeaderAndData(object):
    '''Class to hold channel header and data.

    We don't know what the size of the data will be, so we don't create an
    np.dtype for this structure.  Instead, since it's just a top
    level container, we're fine with just a python class.
    '''

    def __init__(self):
        self.header = np.empty(1, dtype=sChannelHeader)[0]
        self.data = None
