'''readMeasurementHeaderBuffers'''

import logging
import os

import numpy as np

def readMeasurementHeaderBuffers(siemens_dat, num_buffers):
    '''Filler.'''
    buffers = []
    logging.info('Number of parameter buffers: %s', str(num_buffers))
    for _b in range(num_buffers):

        buf = {}
        start = siemens_dat.tell()
        tmp_bufname = siemens_dat.readline().decode(errors='replace')

        idx = tmp_bufname.find('\0')
        if idx > -1:
            siemens_dat.seek(start + idx+1, os.SEEK_SET)
            tmp_bufname = tmp_bufname[:idx]

        logging.info('Buffer Name: %s', tmp_bufname)
        buf['name'] = tmp_bufname
        buflen = np.fromfile(siemens_dat, dtype=np.uint32, count=1)[0] #pylint: disable=E1101
        bytebuf = siemens_dat.read(buflen)
        buf['buf'] = bytebuf.decode(
            'utf-8', errors='replace').replace('\uFFFD', 'X')
        # print('Size of buf:',len(buf['buf']))

        buffers.append(buf)

    return buffers
