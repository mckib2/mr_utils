'''Try to leverage prexisting sorting strategies.'''

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import reverse_cuthill_mckee

from mr_utils.utils.orderings import inverse_permutation
from mr_utils.test_data.phantom import binary_smiley
from mr_utils import view

if __name__ == '__main__':

    # We want to find a sparse representation of X
    ax = 0  # Choosing ax=0 gives marginal improvement when reordering
    X = binary_smiley(512)
    Xinv = np.linalg.pinv(X.T)
    XX = X.dot(X.T)  # Do this to gaurantee symmetry

    # Try finite differences on XX'
    Y = np.diff(XX, axis=ax)
    print(np.sum(np.abs(Y) > 0))
    view(Y)
    recon = np.vstack((XX[:, 0][None, :], Y)).cumsum(axis=ax).dot(Xinv)
    view(recon)

    # Try finite differences on Cuthill-McKee reordered XX'
    Z = sparse.csr_matrix(XX)
    P = reverse_cuthill_mckee(Z, True)
    Z = Z[P, :].A
    A = np.diff(Z, axis=ax)
    print(np.sum(np.abs(A) > 0))
    view(A)
    Pinv = inverse_permutation(P)
    recon = np.vstack((A, Z[:, 0][None, :])).cumsum(axis=ax)[Pinv, :].dot(Xinv)
    view(recon)

    # There's still some distortion going on in both images and severe
    # banding in the Cuthill-McKee reordered set.
