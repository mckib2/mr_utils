'''Testing the MATLAB client connected to remote server.'''

import unittest

import numpy as np

from mr_utils.matlab import client_run, client_get, client_put

class TestMATLABClient(unittest.TestCase):
    '''Simple variable transfer unit tests.'''

    def test_get_variables(self):
        '''Assign variables on remote and then retrieve them.'''

        client_run('A = 3; B = 4; C = 5;')
        data = client_get(['A', 'B', 'C'])
        self.assertEqual(data['A'], 3)
        self.assertEqual(data['B'], 4)
        self.assertEqual(data['C'], 5)

    def test_put_and_get_variables(self):
        '''Assign matrix on remote and then retrieve.'''

        pyArr = np.random.random((2, 2))
        client_put({'pyArr':pyArr})
        client_run('matArr = pyArr')
        matArr = client_get(['matArr'])['matArr']
        self.assertTrue(np.allclose(pyArr, matArr))

    def tearDown(self):
        client_run('clear')

if __name__ == '__main__':
    unittest.main()
