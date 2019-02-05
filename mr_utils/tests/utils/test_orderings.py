'''Tests for reorderings.'''

import unittest

import numpy as np

from mr_utils.utils.orderings import colwise, rowwise, inverse_permutation

class TestOrderings(unittest.TestCase):
    '''Test orderings of matrices to make sure we're doing them right.'''

    def setUp(self):
        self.data = np.random.random((10, 5))

    def test_colwise(self):
        '''Make sure columns are ordered.'''
        idx = colwise(self.data)
        a = self.data.flatten()[idx].reshape(self.data.shape)
        self.assertTrue(np.all(np.diff(a, axis=0) > 0))

    def test_rowwise(self):
        '''Make sure rows get ordered.'''
        idx = rowwise(self.data)
        a = self.data.flatten()[idx].reshape(self.data.shape)
        self.assertTrue(np.all(np.diff(a, axis=1) > 0))

    def test_inverse_colwise(self):
        '''Make sure we make it back from colwise ordering.'''
        idx = colwise(self.data)
        ridx = inverse_permutation(idx)
        self.assertTrue(np.allclose(self.data.flatten()[idx][ridx],
                                    self.data.flatten()))

    def test_inverse_rowwise(self):
        '''Make sure we make it back from rowwise ordering.'''
        idx = rowwise(self.data)
        ridx = inverse_permutation(idx)
        self.assertTrue(np.allclose(self.data.flatten()[idx][ridx],
                                    self.data.flatten()))


if __name__ == '__main__':
    unittest.main()
