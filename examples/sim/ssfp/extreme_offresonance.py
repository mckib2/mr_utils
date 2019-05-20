'''Demonstrate that extreme off-resonance doesn't effect single voxel.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp

class Plotter():
    '''Add some automation to subplots.'''

    def __init__(self, close_loop_def=False, square_def=False):
        self.shape = [0, 0]
        self.xs = []
        self.ys = []
        self.squares = []
        self.close_loop_def = close_loop_def
        self.square_def = square_def

    def add_plot(self, x, y=None, close_loop=None, square=None,
                 loc='lr'):

        # Add either left-right or up-down
        if loc == 'lr':
            self.shape[1] += 1
        elif loc == 'ud':
            self.shape[0] += 1
        else:
            raise ValueError('Only lr or ud are valid.')

        if close_loop is None:
            close_loop = self.close_loop_def

        if square is None:
            square = self.square_def
        self.squares.append(square)

        if not isinstance(x, list):
            x = [x]
            print(x)
            if y is not None:
                y = [y]

        for ii, _xx in enumerate(x):
            if close_loop:
                x[ii] = np.concatenate((x[ii], [x[ii][0]]))
                if y is not None:
                    y[ii] = np.concatenate((y[ii], [y[ii][0]]))

        self.xs.append(x)
        self.ys.append(y)

    def show(self):

        # Make sure we have no zeros
        if self.shape[0] == 0:
            self.shape[0] = 1
        if self.shape[1] == 0:
            self.shape[1] = 1

        # Plot each of the subplots
        for ii in range(len(self.xs)):
            plt.subplot(*self.shape, ii+1)

            for jj, _xx in enumerate(self.xs[ii]):
                if self.ys[ii] is None:
                    plt.plot(self.xs[ii][jj])
                else:
                    plt.plot(self.xs[ii][jj], self.ys[ii][jj])
            if self.squares[ii]:
                plt.axis('square')
        plt.show()

if __name__ == '__main__':

    # Experiment params
    TR = 6e-3
    alpha = np.deg2rad(30)
    npcs = 100
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    M0 = 1
    T1 = .100
    T2 = .030
    df0 = 0
    df1 = 1200
    phi_rf = 0

    I0 = ssfp(T1, T2, TR, alpha, df0, pcs, M0, phi_rf=phi_rf)
    I1 = ssfp(T1, T2, TR, alpha, df1, pcs, M0, phi_rf=phi_rf)

    P = Plotter(close_loop_def=True)
    P.add_plot([I0.real, I1.real], [I0.imag, I1.imag], square=True)
    P.add_plot([np.abs(I0), np.abs(I1)], None)
    P.show()

    # sh = (1, 2)
    # plt.subplot(*sh, 1)
    # plt.plot(I.real, I.imag)
    #
    # plt.subplot(*sh, 2)
    # plt.plot(np.abs(I))
    #
    # plt.show()
