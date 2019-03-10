'''Gadgetron client unit test cases.'''

import unittest

import numpy as np
import h5py
import ismrmrd

from mr_utils.gadgetron import client
from mr_utils.test_data import load_test_data

class GadgetronClientTestCase(unittest.TestCase):
    '''Make sure the client can handle data in several formats.'''

    def setUp(self):
        pass

    def test_client_filename(self):
        '''Give the client only the filename.'''

        # Get the test input data path so we can send file to gadgetron
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'input.h5'
        load_test_data(path, [file], do_return=False)
        filename = '%s/%s' % (path, file)
        data, _header = client(filename)

        # Make sure we get the thing we expected
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'true_output.h5'
        load_test_data(path, [file], do_return=False)
        with h5py.File('%s/%s' % (path, file), 'r') as f:
            true_output_data = f[
                '2018-11-02 20:35:19.785688']['image_0']['data'][:]
        self.assertTrue(np.allclose(data, true_output_data))

    def test_client_ismrmrd_hdf5_input(self):
        '''Give the client the hdf5 file.'''

        # Load in the data so we can pass the client the ismrmrd.Dataset
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'input.h5'
        load_test_data(path, [file], do_return=False)
        filename = '%s/%s' % (path, file)
        dataset = ismrmrd.Dataset(filename, 'dataset', False)
        data, _header = client(dataset)

        # Make sure we still get the thing we expected
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'true_output.h5'
        load_test_data(path, [file], do_return=False)
        with h5py.File('%s/%s' % (path, file), 'r') as f:
            true_output_data = f[
                '2018-11-02 20:35:19.785688']['image_0']['data'][:]
        self.assertTrue(np.allclose(data, true_output_data))

    def test_client_raw_input(self):
        '''Give the client the path to the raw data.'''

        # Give the filename of raw data to the client
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'input.dat'
        load_test_data(path, [file], do_return=False)
        filename = '%s/%s' % (path, file)
        data, _header = client(filename)

        # Make sure the output is the same as when h5 is given
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'true_output.h5'
        load_test_data(path, [file], do_return=False)
        with h5py.File('%s/%s' % (path, file), 'r') as f:
            true_output_data = f[
                '2018-11-02 20:35:19.785688']['image_0']['data'][:]
        self.assertTrue(np.allclose(data, true_output_data))


if __name__ == '__main__':
    unittest.main()
