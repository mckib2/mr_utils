'''Unit tests for Gadgetron configuration generation.'''

import unittest

import numpy as np
from xmldiff import main
import h5py

from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import load_test_data

class GadgetronConfigTestCase(unittest.TestCase):
    '''Verify that mr_util configurations work.'''

    def setUp(self):
        self.config = GadgetronConfig()

        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'grappa_test_data.h5'
        load_test_data(path, [file], do_return=False)
        self.filename = '%s/%s' % (path, file)

    def test_create_default_config(self):
        '''Make sure default config lines up with actual.'''
        config = configs.default()

        path = 'mr_utils/test_data/tests/gadgetron/config/'
        file = 'default.xml'
        load_test_data(path, [file], do_return=False)
        with open('%s/%s' % (path, file), 'r') as f:
            truth = f.read()

        res = len(main.diff_texts(truth.encode(), config.tostring().encode()))
        self.assertTrue(res == 0)

    def test_use_default_config(self):
        '''Send default config to gadgetron to verify that it runs.'''

        # Give the filename of raw data to the client
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'input.dat'
        load_test_data(path, [file], do_return=False)
        filename = '%s/%s' % (path, file)

        # Send gadgetron the local default configuration file
        config = configs.default()
        # print(config)
        # data,header = client(filename,config_local=config.get_filename())
        data, _header = client(filename, config_local=config.tostring())

        # Make sure the output is the same as when h5 is given
        path = 'mr_utils/test_data/tests/gadgetron/client/'
        file = 'true_output.h5'
        load_test_data(path, [file], do_return=False)
        with h5py.File('%s/%s' % (path, file), 'r') as f:
            true_output_data = f[
                '2018-11-02 20:35:19.785688']['image_0']['data'][:]
        self.assertTrue(np.allclose(data, true_output_data))

    def test_use_grappa_cpu_config(self):
        '''Make sure grappa_cpu config lines up with actual.'''
        config = configs.grappa_cpu()
        data, _header = client(self.filename, config_local=config.tostring())
        data_true, _header_true = client(self.filename,
                                         config='grappa_cpu.xml')
        self.assertTrue(np.allclose(data, data_true))

    def test_use_grappa_float_cpu_config(self):
        '''Send grappa_cpu to gadgetron to verify that it runs.'''
        config = configs.grappa_float_cpu()
        data, _header = client(self.filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='grappa_float_cpu.xml')
        self.assertTrue(np.allclose(data, data_true))

    def test_use_grappa_unoptimized_cpu_config(self):
        '''Send grappa_unoptimized_cpu to gadgetron to verify that it runs.'''
        config = configs.grappa_unoptimized_cpu()
        data, _header = client(self.filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='grappa_unoptimized.xml')
        self.assertTrue(np.allclose(data, data_true))

    def test_use_grappa_unoptimized_float_cpu_config(self):
        '''Send grappa_unoptimized_float to gadgetron.'''
        config = configs.grappa_unoptimized_float_cpu()
        data, _header = client(self.filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='grappa_unoptimized_float.xml')
        self.assertTrue(np.allclose(data, data_true))

    def test_use_distributed_default_config(self):
        '''Send distributed_default to gadgetron.'''
        config = configs.distributed_default()
        data, _header = client(self.filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='distributed_default.xml')
        self.assertTrue(np.allclose(data, data_true))

    def test_use_distributed_image_default_config(self):
        '''Send distributed_image_default to Gadgetron.'''
        config = configs.distributed_image_default()
        data, _header = client(self.filename, config_local=config.tostring())
        data_true, _header_true = client(
            self.filename, config='distributed_image_default.xml')
        self.assertTrue(np.allclose(data, data_true))


if __name__ == '__main__':
    unittest.main()
