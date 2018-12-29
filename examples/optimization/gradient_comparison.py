import numpy as np
from mr_utils.test_data.optimization_functions import quadratic,grad_quadratic
from mr_utils.optimization import fd_complex_step,fd_gen_complex_step,cd_gen_complex_step,complex_step_6th_order
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

if __name__ == '__main__':

    N = 1000
    x0 = np.linspace(-100,100,N)
    gs = {
        'grad_quadratic':np.zeros(N),
        'fd_complex_step':np.zeros(N),
        'fd_gen_complex_step':np.zeros(N),
        'cd_gen_complex_step':np.zeros(N),
        'complex_step_6th_order':np.zeros(N)
    }

    # Compute the true gradient
    g_true = np.zeros(N)
    for ii,val in np.ndenumerate(x0):
        g_true[ii] = grad_quadratic(None,np.atleast_1d(val))

    for key in gs.keys():
        for ii,val in np.ndenumerate(x0):
            comp = globals()[key](quadratic,np.atleast_1d(val))[0]
            gs[key][ii] = compare_mse(g_true[ii],comp)

    for key,val in gs.items():
        print('Avg MSE for {:>30s}: {:8e}'.format(key,np.mean(gs[key])))
