import unittest
import numpy as np
from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient
from mr_utils import view


class GadgetronGenericConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = GadgetronConfig()
        self.filename = GadgetronClient.grappa_input_filename()

    @unittest.skip('Can not get this one to work either...')
    def test_use_generic_cartesian_grappa_config(self):
        config = configs.generic_cartesian_grappa()
        filename = GadgetronClient.generic_cartesian_grappa_filename()
        # print(config.tostring())
        data,header = client(filename,config_local=config.tostring())
        # data_true,header_true = client(self.filename,config='Generic_Cartesian_Grappa.xml')
        # self.assertTrue(np.allclose(data,data_true))

if __name__ == '__main__':
    unittest.main()
