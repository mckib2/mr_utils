'''EPI config test cases.'''

import unittest

import numpy as np

from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient

class GadgetronEPIConfigTestCase(unittest.TestCase):
    '''EPI config test cases.'''

    def setUp(self):
        self.config = GadgetronConfig()
        self.filename = GadgetronClient.grappa_input_filename()
        self.epi_filename = GadgetronClient.epi_input_filename()

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
