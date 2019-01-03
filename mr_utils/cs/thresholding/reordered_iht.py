import numpy as np
from mr_utils.utils.printtable import Table
from skimage.measure import compare_mse
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def rIHT(A,y,k,mu=1,tol=1e-8,maxiter=500,x=None,disp=False):
    '''
    '''

    n,N = A.shape[:]
    x_hat = np.zeros(N,dtype=y.dtype)
    r = y.copy()

    if disp:
        table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    for ii in range(int(maxiter)):
        x_hat += mu*np.dot(A.conj().T,r)
        x_hat[np.argsort(np.abs(x_hat))[:-k]] = 0
        r = y - np.dot(A,x_hat)

        stop_criteria = np.linalg.norm(r)/np.linalg.norm(y)
        if disp:
            logging.info(table.row([ ii,stop_criteria,compare_mse(x,x_hat) ]))
        if stop_criteria < tol:
            break

    return(x_hat)
