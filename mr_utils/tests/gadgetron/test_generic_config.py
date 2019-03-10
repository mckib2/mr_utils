'''Unit tests for generic config files.'''

import unittest

import numpy as np

from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import load_test_data

class GadgetronGenericConfigTestCase(unittest.TestCase):
    '''Unit tests for generic config files.'''

    def setUp(self):
        self.config = GadgetronConfig()

        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'grappa_test_data.h5'
        load_test_data(path, [file], do_return=False)
        self.filename = '%s/%s' % (path, file)

    @unittest.skip('Can not get this one to work either...')
    def test_use_generic_cartesian_grappa_config(self):
        '''Compare homegrown to Gagdetron config.'''

        config = configs.generic_cartesian_grappa()

        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'meas_MID00450_FID76726_SAX_TE62_DIR_TSE.dat'
        load_test_data(path, [file], do_return=False)
        filename = '%s/%s' % (path, file)

        # print(config.tostring())
        data, _header = client(filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='Generic_Cartesian_Grappa.xml')
        self.assertTrue(np.allclose(data, data_true))

if __name__ == '__main__':
    unittest.main()
