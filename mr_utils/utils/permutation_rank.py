'''Determining rank of a permutation and generating permutation given rank.

This implementation is due to:
    https://rosettacode.org/wiki/Permutations/Rank_of_a_permutation#Python

See:
    Myrvold, Wendy, and Frank Ruskey. "Ranking and unranking permutations in
    linear time." Information Processing Letters 79.6 (2001): 281-284.
'''

from math import factorial as fact
from random import randrange
from textwrap import wrap

import numpy as np
from tqdm import trange
from scipy.special import factorial

def identity_perm(n):
    '''Generate sequence 0:n-1.'''
    return list(range(n))

def unranker1(n, r, pi):
    '''Given rank produce the corresponding permutation.

    Rank is given by rank1 algorithm of M&R paper.
    '''
    while n > 0:
        n1, (rdivn, rmodn) = n-1, divmod(r, n)
        pi[n1], pi[int(rmodn)] = pi[int(rmodn)], pi[n1]
        n = n1
        r = int(rdivn)
    return pi

def init_pi1(n, pi):
    '''Get the inverse permutation of pi.'''
    pi1 = [-1] * n
    for i in range(n):
        pi1[pi[i]] = i
    return pi1

def ranker1_iter(n, pi, pi1):
    '''Iterative version of ranker1.'''

    result = np.zeros(n, dtype=np.ulonglong)
    for ii in trange(n-1, 0, -1, leave=False, desc='Ranking'):
        s = pi[ii]
        pi[ii], pi[pi1[ii]] = pi[pi1[ii]], pi[ii]
        pi1[s], pi1[ii] = pi1[ii], pi1[s]
        # print(factorial(ii, exact=True))
        result[ii] = s*factorial(ii, exact=True)
    return result


def ranker1(n, pi, pi1):
    '''Rank1 algorithm from M&R paper.'''
    if n == 1:
        return 0
    n1 = n-1
    s = pi[n1]
    pi[n1], pi[pi1[n1]] = pi[pi1[n1]], pi[n1]
    pi1[s], pi1[n1] = pi1[n1], pi1[s]
    return s + n * ranker1(n1, pi, pi1)

def unranker2(n, r, pi):
    '''Given rank produce the corresponding permutation.

    Rank is given by rank2 algorithm of M&R paper.
    '''
    while n > 0:
        n1 = n-1
        s, rmodf = divmod(r, fact(n1))
        pi[n1], pi[int(s)] = pi[int(s)], pi[n1]
        n = n1
        r = int(rmodf)
    return pi

def ranker2_iter(n, pi, pi1):
    '''Iterative version of ranker2.'''
    result = np.uint64(0)
    # result = np.zeros(n-1, dtype=np.uint64)
    for i in trange(n-1, 0, -1, leave=False, desc='Ranking'):
        s = pi[i]
        pi[i], pi[pi1[i]] = pi[pi1[i]], pi[i]
        pi1[s], pi1[i] = pi1[i], pi1[s]
        result += s * fact(i)
        # result[i] = np.uint64(s*fact(i))
    return result

def ranker2(n, pi, pi1):
    '''Ranker2 algorithm from M&R paper.'''
    if n == 1:
        return 0
    n1 = n-1
    s = pi[n1]
    pi[n1], pi[pi1[n1]] = pi[pi1[n1]], pi[n1]
    pi1[s], pi1[n1] = pi1[n1], pi1[s]
    return s * fact(n1) + ranker2(n1, pi, pi1)

def get_random_ranks(permsize, samplesize):
    perms = fact(permsize)
    ranks = set()
    while len(ranks) < samplesize:
        ranks |= set(randrange(perms) for r in range(samplesize - len(ranks)))
    return ranks

def pi2rank(pi, method='rank2', iterative=True):
    '''Return rank of permutation pi.

    pi -- Permutation.
    method -- Which ranking method to use, one of {'rank1', 'rank2'}.
    iterative -- Whether or not to use iterative or recursive version.

    The permutation pi should be a permutation of the list range(n) and contain
    n elements.

    'method' should be one of {'rank1', 'rank2'} corresponding to the two
    schemes presented in the Myrvold and Ruskey paper.  There is an iterative
    version available for both algorithms.

    Implements algorithms from:
        Myrvold, Wendy, and Frank Ruskey. "Ranking and unranking permutations
        in linear time." Information Processing Letters 79.6 (2001): 281-284.
    '''

    # Choose which ranker function to use
    ranker = {
        False: {
            'rank1': ranker1,
            'rank2': ranker2
        },
        True: {
            'rank1': ranker1_iter,
            'rank2': ranker2_iter
        }
    }[iterative][method]

    n = len(pi)
    pi1 = init_pi1(n, pi.copy())
    return ranker(n, pi.copy(), pi1)

def rank2pi(r, n, method='rank2'):
    '''Given rank and permutation length produce the corresponding permutation.

    r -- Rank.
    n -- Lenth of the permutation.
    method -- Which ranking method to use, one of {'rank1', 'rank2'}.

    Implements algorithms from:
        Myrvold, Wendy, and Frank Ruskey. "Ranking and unranking permutations
        in linear time." Information Processing Letters 79.6 (2001): 281-284.
    '''

    # Choose which unranker function to use
    unranker = {
        'rank1': unranker1,
        'rank2': unranker2
    }[method]

    pi = identity_perm(n)
    return unranker(n, r, pi.copy())

def test1(comment, unranker, ranker):
    n, samplesize, n2 = 3, 4, 12
    print(comment)
    perms = []
    for r in range(fact(n)):
        pi = identity_perm(n)
        perm = unranker(n, r, pi)
        perms.append((r, perm))
    for r, pi in perms:
        pi1 = init_pi1(n, pi)
        print('  From rank %2i to %r back to %2i' % (
            r, pi, ranker(n, pi[:], pi1)))
    print('\n  %i random individual samples of %i items:' % (samplesize, n2))
    for r in get_random_ranks(n2, samplesize):
        pi = identity_perm(n2)
        print('    ' + ' '.join('%2i' % i for i in unranker(n2, r, pi)))
    print('')

def test2(comment, unranker):
    samplesize, n2 = 4, 144
    print(comment)
    print('  %i random individual samples of %i items:' % (samplesize, n2))
    for r in get_random_ranks(n2, samplesize):
        pi = identity_perm(n2)
        print('    ' + '\n      '.join(wrap(repr(unranker(n2, r, pi)))))
    print('')

if __name__ == '__main__':
    test1('First ordering:', unranker1, ranker1)
    test1('Second ordering:', unranker2, ranker2)
    test2('First ordering, large number of perms:', unranker1)
