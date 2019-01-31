'''Unit tests for view module.

The view function does a lot of things.  To help with debugging, it has the
'test_run' argument that doesn't plot anything, instead it sends back an info
dictionary with all the debugging variables included.
'''

import unittest

from mr_utils import view

class TestView(unittest.TestCase):
    '''Make sure view is doing what we tell it to do.'''

    def setUp(self):
        from mr_utils.test_data import ViewTestData
        self.npy_filename = ViewTestData.ssfp_ankle_te_6_pc_0()

    def test_view_load_vanilla_npy(self):
        '''Simple test case of viewing single .npy image only.'''
        info = view(self.npy_filename, test_run=True)
        self.assertTrue(info['data'].size)

    def test_view_load_npy_with_load_opts(self):
        '''Load in .npy with invalid option.'''
        with self.assertRaises(TypeError):
            view(self.npy_filename, load_opts={'not':'an option'},
                 test_run=True)

    def test_view_coil_combine_walsh(self):
        '''Coil combine the image using the walsh iterative method.'''
        info = view(self.npy_filename, fft=True, fft_axes=(0, 1),
                    coil_combine_axis=-1, test_run=True)
        self.assertTrue(info['data'].shape == (256, 256))

    def test_view_coil_combine_pca(self):
        '''Coil combine the image using the PCA method.'''
        info = view(self.npy_filename, fft=True, fft_axes=(0, 1),
                    coil_combine_axis=-1, coil_combine_method='pca',
                    coil_combine_opts={'n_components':1}, test_run=True)
        self.assertTrue(info['data'].shape == (260, 260))

    def test_view_coil_combine_inati(self):
        '''Coil combine using the inati iterative method.'''
        info = view(self.npy_filename, fft=True, fft_axes=(0, 1),
                    coil_combine_axis=-1, coil_combine_method='inati',
                    test_run=True)
        self.assertTrue(info['data'].shape == (256, 256))


if __name__ == '__main__':
    unittest.main()
