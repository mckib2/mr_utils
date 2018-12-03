import unittest
from mr_utils.matlab import Client
import numpy as np

def start_matlab():
    client = Client()

    # Add some example variables
    client.run('A = 3;')
    client.run('B = 4;')
    client.run('C = sqrt(A^2 + B^2)')

    return(client)

class TestMATLABClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Only start MATLAB once for the test suite because it takes so long to
        # load
        super(TestMATLABClient,cls).setUpClass()
        cls.client = start_matlab()

    def test_get_variables_fail(self):
        with self.assertRaises(ValueError):
            self.client.get([ 'D' ])

    def test_get_variables(self):
        data = self.client.get([ 'A','B','C' ])
        self.assertEqual(data['A'],3)
        self.assertEqual(data['B'],4)
        self.assertEqual(data['C'],5)

    def test_put_variables(self):
        pyArr = np.random.random((2,2))
        self.client.put({'pyArr':pyArr})
        self.client.run('matArr = pyArr')
        matArr = self.client.get([ 'matArr' ])['matArr']
        self.assertTrue(np.allclose(pyArr,matArr))

    @classmethod
    def tearDownClass(cls):
        cls.client.run('who')
        cls.client.exit()

if __name__ == '__main__':
    unittest.main()
