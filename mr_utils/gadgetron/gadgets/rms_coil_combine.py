'''Example Python Gadget.

See:
    https://github.com/gadgetron/gadgetron/blob/master/gadgets/python/gadgets/rms_coil_combine.py
'''

import numpy as np
try:
    from gadgetron import Gadget  # pylint: disable=E0401
except ModuleNotFoundError:
    Gadget = object

class RMSCoilCombine(Gadget):
    '''Gadget that using RMS method to combine coils.'''

    def process_config(self, _cfg):
        '''Process XML configuration file.'''
        print("RMS Coil Combine, Config ignored")

    def process(self, h, im):
        '''Process the data, combine coils.'''

        combined_image = np.sqrt(np.sum(np.square(np.abs(im)), axis=-1))

        print("RMS coil", im.shape, combined_image.shape)
        h.channels = 1
        self.put_next(h, combined_image.astype('complex64'))
        return 0
