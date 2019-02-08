'''Find T1, T2, theta given N bSSFP acquisitons.'''

import numpy as np
from scipy.optimize import least_squares

from mr_utils.sim.ssfp import ssfp
from mr_utils.utils import sos

def fun(x, y, TR, alpha, M0):
    '''Residual.'''
    y00 = ssfp(x[0], x[1], TR, alpha, field_map=x[2], phase_cyc=0, M0=M0)
    y01 = ssfp(x[0], x[1], TR, alpha, field_map=x[2], phase_cyc=np.pi, M0=M0)
    y0 = np.array((y00.real, y01.real, y00.imag, y01.imag))
    return y0 - y

def M0fun(x, y, T1, T2, theta, TR, alpha):
    '''Residual for M0 estimation.'''
    y00 = ssfp(T1, T2, TR, alpha, field_map=theta, phase_cyc=0, M0=x[3])
    y01 = ssfp(T1, T2, TR, alpha, field_map=theta, phase_cyc=np.pi, M0=x[3])
    y0 = sos((y00, y01))
    return y0 - y

if __name__ == '__main__':

    # Acquisiton parameters
    TR = 6e-3
    bnds = ((0.8, .04, -1/TR, 0.0),
            (1.0, .06, 1/TR, 1.0))
    alpha = 0.174533 #np.pi/3

    # Average over a number of iterations
    niter = 1000
    err = np.zeros((niter, 4))
    for jj in range(niter):

        # True simulation parameters
        T1 = np.random.random(1)[0]*(bnds[1][0] - bnds[0][0]) + bnds[0][0]
        T2 = np.random.random(1)[0]*(bnds[1][1] - bnds[0][1]) + bnds[0][1]
        df = np.random.random(1)[0]*(bnds[1][2] - bnds[0][2]) + bnds[0][2]
        M0 = np.random.random(1)[0]*(bnds[1][3] - bnds[0][3]) + bnds[0][3]

        # Simulate acquisiton of two phase cycles
        y_train0 = ssfp(T1, T2, TR, alpha, field_map=df, phase_cyc=0, M0=M0)
        y_train1 = ssfp(T1, T2, TR, alpha, field_map=df, phase_cyc=np.pi,
                        M0=M0)
        y_train = np.array(
            (y_train0.real, y_train1.real, y_train0.imag, y_train1.imag))
        M0_train = sos((y_train0, y_train1))

        # Initialize
        x0 = np.zeros(4)  # x0 = (T1, T2, theta, M0)
        loss = ['linear', 'soft_l1', 'huber', 'cauchy', 'arctan']
        weights = [1, 2]
        x0[0] = (bnds[1][0] + bnds[0][0])/2
        x0[1] = (bnds[1][1] + bnds[0][1])/2
        x0[2] = (bnds[1][2] + bnds[0][2])/2
        x0[3] = M0_train  # Guess M0 is SOS

        # Do a 2 step update for a fixed number of steps:
        for ii in range(10):
            # Solve for M0, only to modify x[3]
            x = least_squares(M0fun, x0, bounds=bnds,
                              loss=loss[4], f_scale=1e-2,
                              args=(M0_train, *x0[:3], TR, alpha))['x']
            x0[3] = np.average((x0[3], x[3]), weights=weights)

            # Solve for T1, T2, theta, only to modify x[0,1,2]
            x = least_squares(fun, x0, bounds=bnds,
                              loss=loss[4], f_scale=1e-2,
                              args=(y_train, TR, alpha, x0[3]))['x']
            x0[:3] = np.average((x0[:3], x[:3]), weights=weights, axis=0)

        x = np.array((T1, T2, df, M0))
        err[jj, ...] = [100*(a - b)/((a + b)/2) for a, b in zip(x, x0)]
        print(jj, err[jj, ...])

    print('Totals:')
    print('    avg:', np.mean(np.abs(err), axis=0))
    print('    std:', np.std(np.abs(err), axis=0))

    # Totals:
    # avg: [ 10.20648767  14.31978469 118.32378057   9.12910694]
    # std: [   6.58689497   11.34622737 1456.27207552   11.82318381]
