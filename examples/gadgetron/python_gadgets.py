'''Send data to Gadgetron to be processed using python Gadgets.'''

from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient
from mr_utils.gadgetron.configs import python_short
from mr_utils import view

if __name__ == '__main__':

    config = python_short()
    data = GadgetronClient.input_filename()
    im, hdr = client(data, config_local=config.tostring(), verbose=True)
    # im, hdr = client(data, config="python_short.xml", verbose=True)

    view(im)
