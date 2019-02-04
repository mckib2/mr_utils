'''Find T1, T2, theta given N bSSFP acquisitons.'''

import numpy as np
from scipy.optimize import least_squares

from mr_utils.sim.ssfp import ssfp

def fun(x, y, TR, alpha):
    '''Residual.'''
    y0 = ssfp(x[0], x[1], TR, alpha, field_map=x[2], phase_cyc=0, M0=1)
    y0 = np.stack((y0.real, y0.imag))
    return y0 - y


if __name__ == '__main__':

    TR = 6e-3
    alpha = np.pi/3
    T1 = 1.8
    T2 = .8
    df = .2/TR
    M0 = 1

    y_train = ssfp(T1, T2, TR, alpha, field_map=df, phase_cyc=0, M0=M0)
    y_train = np.stack((y_train.real, y_train.imag))
    x0 = np.ones(3)
    bounds = ((1., .1, -1/TR), (2., 1., 1/TR))
    res_lsq = least_squares(fun, x0, bounds=bounds, args=(y_train, TR, alpha))

    loss = ['linear', 'soft_l1', 'huber', 'cauchy', 'arctan']
    res_robust = least_squares(fun, x0, bounds=bounds, loss=loss[4],
                               f_scale=1e-2, args=(y_train, TR, alpha))

    print(res_lsq)
    print(res_robust)
    print(T1, T2, df)
