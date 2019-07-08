'''Test out some ideas about 4-pt ellipses.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.utils import plot_conic

if __name__ == '__main__':

    # Define an underlying ellipse
    Cu = np.zeros(6)
    Cu[0] = 2
    Cu[1] = 3
    Cu[2] = 4
    Cu[3] = 5
    Cu[4] = 3
    Cu[5] = 2

    # Now assume we only have four evenly spaced points
    xu, yu = plot_conic(Cu)
    pts = np.roll(
        np.arange(xu.size), np.random.randint(0, xu.size))
    pts = pts[1::int(pts.size/4)]
    x, y = xu[pts], yu[pts]

    # # Now get best linear fit to try and identify major-axis
    # A = np.vstack([x, np.ones(len(x))]).T
    # m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    # plt.plot(x, m*x + c, 'r', label='Fitted line')

    plt.plot(xu, yu, label='underlying')
    plt.plot(x, y, '*', label='samples')

    plt.plot(x[[0, 1]], y[[0, 1]])
    plt.plot(x[[2, 3]], y[[2, 3]])
    plt.plot(x[[0, 3]], y[[0, 3]])
    plt.plot(x[[1, 2]], y[[1, 2]])

    plt.axis('square')
    plt.legend()
    plt.show()
