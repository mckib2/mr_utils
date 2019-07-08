'''Use a representative exponential growth curve to find permutation.
'''

from itertools import permutations

import numpy as np
from scipy.fftpack import dct

from mr_utils.utils import gini

if __name__ == '__main__':

    # Make curve
    nts = 6
    T1 = 1.2
    t = np.linspace(0, 3*T1, nts+1)[1:]
    s = 1 - np.exp(-1*t/T1)

    perms = np.array(list(set(permutations(list(range(s.size))))))
    gini_scores = np.zeros(perms.shape[0])
    for ii, p in enumerate(perms):
        gini_scores[ii] = gini(dct(s[p], norm='ortho'))
        # gini_scores[ii] = gini(np.diff(s[p], n=1, prepend=0))
        # gini_scores[ii] = 1/np.linalg.norm(np.diff(s[p], n=1, prepend=0), ord=1)
        # gini_scores[ii] = 1/np.sum(np.abs(np.diff(s[p], prepend=0)))

    print(perms[np.argmax(gini_scores)])
