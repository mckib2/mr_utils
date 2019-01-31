'''Coil combination using PCA unit tests.'''

import unittest

from sklearn.decomposition import PCA
from skimage.data import lfw_subset
import numpy as np

from mr_utils.coils.coil_combine import python_pca

class TestPCA(unittest.TestCase):
    '''Test PCA implmentations.'''

    def test_python_pca(self):
        '''Make sure that python implementation matches sklearn's.'''

        X = lfw_subset()[:10, :, :].reshape((10, -1)).transpose((1, 0))
        n_components = 2
        Y_py = python_pca(X, n_components)
        Y_ski = PCA(n_components=n_components, whiten=False).fit_transform(X)

        # Same within scale factor of -1
        self.assertTrue(np.allclose(np.abs(Y_py), np.abs(Y_ski)))


if __name__ == '__main__':
    unittest.main()
