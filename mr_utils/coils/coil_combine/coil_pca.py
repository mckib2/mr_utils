'''Coil compression using principal component analysis.'''

import logging

import numpy as np
from sklearn.decomposition import PCA

def python_pca(X, n_components=False):
    '''Python implementation of principal component analysis.

    To verify I know what sklearn's PCA is doing.
    '''

    M = np.mean(X.T, axis=1)
    C = X - M
    V = np.cov(C.T)
    _values, vectors = np.linalg.eig(V)
    P = vectors.T.dot(C.T)[:n_components, :].T

    return P

def coil_pca(
        coil_ims,
        coil_dim=-1,
        n_components=4,
        give_explained_var=False,
        debug_level=logging.WARNING):
    '''Reduce the dimensionality of the coil dimension using PCA.

    coil_dim -- Coil axis, default is last axis.
    coil_ims -- Coil images.
    n_components -- How many principal components to keep.
    give_explained_var -- Return explained variance for real,imag decomposition
    debug_level -- Verbosity level to set logging module.

    give_explained_var=True will return (coil_ims_pca,expl_var). expl_var is a
    complex valued 1D vector representing:
        cumsum(pca_real.explained_variance_ratio_) +
                                  1j*cumsum(pca_imag.explained_variance_ratio_)

    Thus, if you were so inclined, you could take a look and see how many
    components you'd need to explain the variance up to some percentage.
    '''

    # Every day I'm logging...
    logging.basicConfig(format='%(levelname)s: %(message)s', level=debug_level)
    logging.info('Starting coil_pca: initial size: %s', str(coil_ims.shape))

    # Get data in form (n_samples,n_features)
    coil_ims = np.moveaxis(coil_ims, coil_dim, -1)
    n_features = coil_ims.shape[-1]
    im_shape = coil_ims.shape[:-1]
    coil_ims = np.reshape(coil_ims, (-1, n_features))
    logging.info('Number of features: %d', n_features)

    # Do PCA on both real/imag parts
    logging.info('Performing PCA on real/imag parts...')
    pca_real = PCA(n_components=n_components)
    pca_imag = PCA(n_components=n_components)
    coil_ims_real = pca_real.fit_transform(coil_ims.real)
    coil_ims_imag = pca_imag.fit_transform(coil_ims.imag)

    coil_ims_pca = (coil_ims_real + 1j*coil_ims_imag).reshape(
        (*im_shape, n_components))

    # Move coil dim back to where it was
    coil_ims_pca = np.moveaxis(coil_ims_pca, -1, coil_dim)

    logging.info('Resulting size: %s', str(coil_ims_pca.shape))
    logging.info('Number of components: %d', n_components)

    if give_explained_var:
        logging.info((
            'Returning explained_variance_ratio for both real and imag PCA'
            ' decompositions.'))
        logging.info((
            'Do mr_utils.view(expl_var.real) to see the plot for the real'
            'part.'))
        expl_var = (np.cumsum(pca_real.explained_variance_ratio_)
                    + 1j*np.cumsum(pca_imag.explained_variance_ratio_))
        return(coil_ims_pca, expl_var)

    # else...
    return coil_ims_pca

if __name__ == '__main__':
    pass
