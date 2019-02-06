'''Tests for reorderings.'''

import unittest

import numpy as np
from scipy.linalg import hadamard

from mr_utils.utils.orderings import colwise, rowwise, inverse_permutation, \
    random_match, random_search


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

    def test_random_match(self):
        '''Try to match a matrix as closely as possible.'''

        N = 16
        T = hadamard(N)
        x = np.random.randn(N, N)
        idx, f = random_match(x, T, return_sorted=True)
        self.assertTrue(np.allclose(x.flatten()[idx].reshape(f.shape), f))

        # Doesn't always pass...
        self.assertTrue(np.sum(T - np.sign(f).astype(int) != 0) < N**2/4)

    def test_random_search_matrix(self):
        '''Make sure that we increase sparsity when using transform matrix.'''

        N = 16
        T = hadamard(N)
        x = np.random.randn(N)
        idx = random_search(x, T, k=1e4, compare='l1', disp=False)

        # import matplotlib.pyplot as plt
        # plt.plot(-np.sort(-np.abs(T.dot(x))))
        # plt.plot(-np.sort(-np.abs(T.dot(x[idx]))), '--')
        # plt.show()

        norm1 = np.linalg.norm(T.dot(x), ord=1)
        norm2 = np.linalg.norm(T.dot(x[idx]), ord=1)

        self.assertTrue(norm1 >= norm2)

    def test_random_search_function(self):
        '''Make sure that we increase sparsity when using transform function.
        '''

        N = 16
        T = lambda x: hadamard(N).dot(x)
        x = np.random.randn(N)
        idx = random_search(x, T, k=1e4, compare='l1', disp=False)

        # import matplotlib.pyplot as plt
        # plt.plot(-np.sort(-np.abs(T(x))))
        # plt.plot(-np.sort(-np.abs(T(x[idx]))), '--')
        # plt.show()

        norm1 = np.linalg.norm(T(x), ord=1)
        norm2 = np.linalg.norm(T(x[idx]), ord=1)

        self.assertTrue(norm1 >= norm2)


if __name__ == '__main__':
    unittest.main()
