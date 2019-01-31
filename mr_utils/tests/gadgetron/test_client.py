'''Gadgetron client unit test cases.'''

import unittest

import numpy as np

from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient

class GadgetronClientTestCase(unittest.TestCase):
    '''Make sure the client can handle data in several formats.'''

    def setUp(self):
        pass

    def test_client_filename(self):
        '''Give the client only the filename.'''

        # Get the test input data path so we can send file to gadgetron
        filename = GadgetronClient.input_filename()
        data, _header = client(filename)

        # Make sure we get the thing we expected
        true_output_data = GadgetronClient.true_output_data()
        self.assertTrue(np.allclose(data, true_output_data))

    def test_client_ismrmrd_hdf5_input(self):
        '''Give the client the hdf5 file.'''

        # Load in the data so we can pass the client the ismrmrd.Dataset
        dataset = GadgetronClient.input_h5()
        data, _header = client(dataset)

        # Make sure we still get the thing we expected
        true_output_data = GadgetronClient.true_output_data()
        self.assertTrue(np.allclose(data, true_output_data))

    def test_client_raw_input(self):
        '''Give the client the path to the raw data.'''

        # Give the filename of raw data to the client
        filename = GadgetronClient.raw_input_filename()
        data, _header = client(filename)

        # Make sure the output is the same as when h5 is given
        true_output_data = GadgetronClient.true_output_data()
        self.assertTrue(np.allclose(data, true_output_data))


if __name__ == '__main__':
    unittest.main()
