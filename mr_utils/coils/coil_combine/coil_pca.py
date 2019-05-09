'''Coil compression using principal component analysis.'''

import logging

import numpy as np
from sklearn.decomposition import PCA

def python_pca(X, n_components=False):
    '''Python implementation of principal component analysis.

    To verify I know what sklearn's PCA is doing.

    Parameters
    ----------
    X : array_like
        Matrix to perform PCA on.
    n_components : int, optional
        Number of components to keep.

    Returns
    -------
    P : array_like
        n_component principal components of X.
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
        real_imag=True,
        debug_level=logging.WARNING):
    '''Reduce the dimensionality of the coil dimension using PCA.

    Parameters
    ----------
    coil_ims : array_like
        Coil images.
    coil_dim : int, optional
        Coil axis, default is last axis.
    n_components : int, optional
        How many principal components to keep.
    give_explained_var : bool, optional
        Return explained variance for real,imag decomposition
    real_imag : bool, optional
        Perform PCA on real/imag parts separately or mag/phase.
    debug_level : logging_level, optional
        Verbosity level to set logging module.

    Returns
    -------
    coil_ims_pca : array_like
        Compressed coil images representing n_components principal
        components.
    expl_var : array_like, optional
        complex valued 1D vector representing explained variance.  Is
        returned if `give_explained_var=True`
    '''

    # Every day I'm logging...
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=debug_level)
    logging.info(
        'Starting coil_pca: initial size: %s', str(coil_ims.shape))

    # Get data in form (n_samples,n_features)
    coil_ims = np.moveaxis(coil_ims, coil_dim, -1)
    n_features = coil_ims.shape[-1]
    im_shape = coil_ims.shape[:-1]
    coil_ims = np.reshape(coil_ims, (-1, n_features))
    logging.info('Number of features: %d', n_features)

    # Do PCA on both real/imag parts
    if real_imag:
        logging.info('Performing PCA on real/imag parts...')
        pca_real = PCA(n_components=n_components)
        pca_imag = PCA(n_components=n_components)
        coil_ims_real = pca_real.fit_transform(coil_ims.real)
        coil_ims_imag = pca_imag.fit_transform(coil_ims.imag)

        coil_ims_pca = (coil_ims_real + 1j*coil_ims_imag).reshape(
            (*im_shape, n_components))
    else:
        # Do PCA on magnitude and phase
        logging.info('Performing PCA on mag/phase...')
        pca_mag = PCA(n_components=n_components)
        pca_phase = PCA(n_components=n_components)
        coil_ims_mag = pca_mag.fit_transform(np.abs(coil_ims))
        coil_ims_phase = pca_phase.fit_transform(np.angle(coil_ims))

        coil_ims_pca = (
            coil_ims_mag*np.exp(1j*coil_ims_phase)).reshape(
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
