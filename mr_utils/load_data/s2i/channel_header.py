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
