'''Store data and header for each channel.'''

import numpy as np

from mr_utils.load_data.s2i import sMDH, ChannelHeaderAndData, sChannelHeader

def readChannelHeaders(siemens_dat, VBFILE, scanhead):
    '''Read the headers for the channels.'''

    nchannels = scanhead['ushUsedChannels']
    nsamples = scanhead['ushSamplesInScan']
    channels = np.empty(nchannels, dtype=object)
    for c in range(nchannels):

        # If we have VB, then we need to shovel all the MDH info into the
        # sChannelHeader
        if VBFILE:
            if c > 0:
                mdh = np.fromfile(siemens_dat, dtype=sMDH, count=1)[0]
            else:
                mdh = {'lMeasUID': 0, 'ulScanCounter': 0, 'ushChannelId': 0}

            channels[c] = ChannelHeaderAndData()
            channels[c].header['ulTypeAndChannelLength'] = 0
            channels[c].header['lMeasUID'] = mdh['lMeasUID']
            channels[c].header['ulScanCounter'] = mdh['ulScanCounter']
            channels[c].header['ulReserved1'] = 0
            channels[c].header['ulSequenceTime'] = 0
            channels[c].header['ulUnused2'] = 0
            channels[c].header['ulChannelId'] = mdh['ushChannelId']
            channels[c].header['ulUnused3'] = 0
            channels[c].header['ulCRC'] = 0

        else:
            # If not VB, then we can read the sChannelHeader directly:
            channels[c].header = np.fromfile(
                siemens_dat, dtype=sChannelHeader, count=1)[0]

        # Read the channel data in as complex64 (float32 + 1j*float32)
        channels[c].data = np.fromfile(
            siemens_dat, dtype=np.complex64, count=nsamples) #pylint: disable=E1101

    return channels
