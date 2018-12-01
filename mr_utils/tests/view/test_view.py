import unittest
from mr_utils import view

class TestView(unittest.TestCase):

    def setUp(self):
        from mr_utils.test_data import ViewTestData,GadgetronClient
        self.npy_filename = ViewTestData.ssfp_ankle_te_6_pc_0()

    def test_view_load_vanilla_npy(self):
        info = view(self.npy_filename,test_run=True)
        self.assertTrue(info['data'].size)

    def test_view_load_npy_with_load_opts(self):
        with self.assertRaises(TypeError):
            info = view(self.npy_filename,load_opts={ 'not':'an option' },test_run=True)

if __name__ == '__main__':
    unittest.main()
