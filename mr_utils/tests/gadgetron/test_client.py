import unittest
from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=FutureWarning)
    import ismrmrd

class GadgetronClientTestCase(unittest.TestCase):

    def setUp(self):
        self.address = '172.17.0.2'
        self.port = 9002

    def test_client_filename(self):

        # Get the test input data path so we can send file to gadgetron
        filename = GadgetronClient.input_filename()
        data,header = client(filename,address=self.address,port=self.port,verbose=False)

        # Make sure we get the thing we expected
        true_output_data = GadgetronClient.true_output_data()
        assert(np.allclose(data,true_output_data))

    def test_client_ismrmrd_hdf5_input(self):

        # Load in the data so we can pass the client the ismrmrd.Dataset
        dataset = GadgetronClient.input_h5()
        data,header = client(dataset,address=self.address,port=self.port)

        # Make sure we still get the thing we expected
        true_output_data = GadgetronClient.true_output_data()
        assert(np.allclose(data,true_output_data))

    def test_client_raw_input(self):

        # Give the filename of raw data to the client
        filename = GadgetronClient.raw_input_filename()
        data,header = client(filename,address=self.address,port=self.port)

        # Make sure the output is the same as when h5 is given
        true_output_data = GadgetronClient.true_output_data()
        assert(np.allclose(data,true_output_data))


if __name__ == '__main__':
    unittest.main()
