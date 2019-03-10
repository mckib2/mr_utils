'''EPI config test cases.'''

import unittest

import numpy as np

from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import load_test_data

class GadgetronEPIConfigTestCase(unittest.TestCase):
    '''EPI config test cases.'''

    def setUp(self):
        self.config = GadgetronConfig()

        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'grappa_test_data.h5'
        load_test_data(path, [file], do_return=False)
        self.filename = '%s/%s' % (path, file)

        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'epi_2d_out_20161020_pjv.h5'
        load_test_data(path, [file], do_return=False)
        self.epi_filename = '%s/%s' % (path, file)

    @unittest.skip('We do not have the right data to do this')
    def test_use_epi_config(self):
        '''Compare results of homegrown config and gadgetron config.'''

        config = configs.epi_gtplus_grappa()
        data, _header = client(
            self.epi_filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.epi_filename, config='epi_gtplus_grappa.xml',
            in_group='/epi.xml/image_0')
        self.assertTrue(np.allclose(data, data_true))

if __name__ == '__main__':
    unittest.main()
