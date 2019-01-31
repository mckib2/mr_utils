'''Unit tests for generic config files.'''

import unittest

import numpy as np

from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient

class GadgetronGenericConfigTestCase(unittest.TestCase):
    '''Unit tests for generic config files.'''

    def setUp(self):
        self.config = GadgetronConfig()
        self.filename = GadgetronClient.grappa_input_filename()

    @unittest.skip('Can not get this one to work either...')
    def test_use_generic_cartesian_grappa_config(self):
        '''Compare homegrown to Gagdetron config.'''

        config = configs.generic_cartesian_grappa()
        filename = GadgetronClient.generic_cartesian_grappa_filename()
        # print(config.tostring())
        data, _header = client(filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='Generic_Cartesian_Grappa.xml')
        self.assertTrue(np.allclose(data, data_true))

if __name__ == '__main__':
    unittest.main()
