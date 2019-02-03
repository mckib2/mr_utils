'''Acquire pairs of points that are close together (i.e., dtheta small).

Given a spectral profile, d(theta), any two points sampled along d(theta), say
m0 and m1, do not constrain d(theta) to single possible profile.  Normally, we
sample at theta=0 and theta=180 degrees and then do a sum of squares for
optimal SNR banding reduction.  However, if we choose dtheta small, then we can
constrain d(theta) by two points plus the approximate derivative,
d/dtheta d(theta), at (theta1 - theta0)/2.

This script attempts to show that this will limit possible realizations of
d(theta) further than just taking two points 180 degrees apart.  We will also
try to apply the elliptical signal model with pairs of points taken at small
theta intervals.
'''

from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    # Generate a sample tissue
    pass
