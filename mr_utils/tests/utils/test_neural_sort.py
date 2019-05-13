'''Test implementation of stochastic sorting function.'''

import unittest

import numpy as np
import tensorflow as tf

from mr_utils.utils import neural_sort

def bl_matmul(A, B):
    '''
    Notes
    -----
    Function to do [1]_.
    '''
    return tf.einsum('mij,jk->mik', A, B)

def reference_implementation(s, tau=1):
    '''

    Returns
    -------
    P : Tensor
        Tensorflow Tensor object

    Notes
    -----
    This is the provided implementation [1]_ given by the authors of
    [2]_.

    References
    ----------
    .. [1] https://github.com/ermongroup/neuralsort/blob/master/tf/
           util.py

    .. [2] Grover, Aditya, et al. "Stochastic optimization of sorting
           networks via continuous relaxations." arXiv preprint
           arXiv:1903.08850 (2019).
    '''

    s = tf.cast(s, dtype=tf.float32)

    A_s = s - tf.transpose(s, perm=[0, 2, 1])
    A_s = tf.abs(A_s)
    # As_ij = |s_i - s_j|

    n = tf.shape(s)[1]
    one = tf.ones((n, 1), dtype=tf.float32)

    B = bl_matmul(A_s, one @ tf.transpose(one))
    # B_:k = (A_s)(one)

    K = tf.range(n) + 1
    # K_k = k

    C = bl_matmul(s, tf.expand_dims(
        tf.cast(n + 1 - 2 * K, dtype=tf.float32), 0))
    # C_:k = (n + 1 - 2k)s

    P = tf.transpose(C - B, perm=[0, 2, 1])
    # P_k: = (n + 1 - 2k)s - (A_s)(one)

    P = tf.nn.softmax(P / tau, -1)
    # P_k: = softmax( ((n + 1 - 2k)s - (A_s)(one)) / tau )

    return P


class TestNeuralSort(unittest.TestCase):
    '''Verification unit tests for my implementation.'''

    def __setUp__(self):
        pass

    def test_1d_random(self):
        '''Sort a 1d random sequence.'''

        N = 100
        s = np.random.normal(0, 1, N)
        tau = 1
        P0 = neural_sort(s, tau=tau)
        P1 = reference_implementation(s[None, :, None], tau=tau)

        # P1 is a tensor object, so we need to evaluate it
        P1 = tf.Session().run(P1).squeeze()

        # Get the sorting indices:
        idx0 = np.argmax(P0, axis=0)
        idx1 = np.argmax(P1, axis=0)
        self.assertTrue(np.allclose(idx0, idx1))

if __name__ == '__main__':
    unittest.main()
