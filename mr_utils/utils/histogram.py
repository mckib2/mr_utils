'''Some functions for working with histograms.
'''

import numpy as np
from scipy.spatial.distance import cosine
from scipy.spatial.distance import jensenshannon
from scipy.stats import wasserstein_distance

def dH(H1, H2, mode='l2'):
    '''Histogram metrics.

    H1, H2 -- 1d histograms with matched bins.
    mode -- Metric to use.

    Similar bins means the same number and size over the same range.

    Modes:
        l2 -- Euclidean distance
        l1 -- Manhattan distance
        vcos -- Vector cosine distance
        intersect -- Histogram intersection distance
        chi2 -- Chi square distance
        jsd -- Jensen-Shannan Divergence
        emd -- Earth Mover's Distance

    Issues:
        I'm not completely convinced that intersect is doing the right thing.

    The quality of the metric will depend a lot on the qaulity of the
    histograms themselves.  Obviously more samples and well-chosen bins will
    help out in the comparisons.
    '''

    val = None
    if mode == 'l2':
        val = np.linalg.norm(H1 - H2, ord=2)
    if mode == 'l1':
        val = np.linalg.norm(H1 - H2, ord=1)
    if mode == 'vcos':
        val = cosine(H1, H2)
    if mode == 'intersect':
        val = np.sum(np.min(np.stack((H1, H2)), axis=0))
    if mode == 'chi2':
        a = 2*((H1 - H2)**2).astype(float)
        b = H1 + H2
        val = np.sum(np.divide(a, b, out=np.zeros_like(a), where=b != 0))
    if mode == 'jsd':
        val = jensenshannon(H1, H2)
    if mode == 'emd':
        val = wasserstein_distance(H1, H2)

    if val is None:
        raise NotImplementedError()
    return val

def hist_match(source, template):
    '''
    Adjust the pixel values of a grayscale image such that its histogram
    matches that of a target image

    Arguments:
    -----------
        source: np.ndarray
            Image to transform; the histogram is computed over the flattened
            array
        template: np.ndarray
            Template image; can have different dimensions to source
    Returns:
    -----------
        matched: np.ndarray
            The transformed output image

    See:
        https://stackoverflow.com/questions/32655686/histogram-matching-of-two-images-in-python-2-x
    '''

    oldshape = source.shape
    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and
    # counts
    _s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                             return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)
