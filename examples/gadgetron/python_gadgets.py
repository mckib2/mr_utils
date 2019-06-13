'''Send data to Gadgetron to be processed using python Gadgets.'''

from mr_utils.gadgetron import client
from mr_utils.test_data import load_test_data
from mr_utils.gadgetron.configs import python_short
from mr_utils import view

if __name__ == '__main__':

    path = 'mr_utils/test_data/tests/gadgetron/client/'
    file = 'input.h5'
    load_test_data(path, [file], do_return=False)
    data = '%s/%s' % (path, file)

    config = python_short()
    im, hdr = client(
        data, config_local=config.tostring(), verbose=True)
    # im, hdr = client(data, config="python_short.xml", verbose=True)

    view(im)
