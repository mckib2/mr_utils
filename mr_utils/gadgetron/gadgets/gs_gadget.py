'''Gadgetron gadget, config file to do GS recon on each coil of GRAPPA recon.
'''

import numpy as np
try:
    from gadgetron import Gadget
except ModuleNotFoundError:
    Gadget = object
# from mr_utils.recon.ssfp import gs_recon

class GS_2d(Gadget):

    def process_config(self, cfg):
        print("RMS Coil Combine, Config ignored")

    def process(self, hdr, ims):

        # Coil dimension is last dimension of images
        # recon = gs_recon()

        combined_image = np.sqrt(
            np.sum(np.square(np.abs(ims)), axis=(len(ims.shape)-1)))

        print("RMS coil", ims.shape, combined_image.shape)
        hdr.channels = 1
        self.put_next(hdr, combined_image.astype('complex64'))
        return 0

if __name__ == '__main__':
    pass
