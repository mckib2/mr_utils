'''Simple cylindrical phantoms generated with different contrasts.'''

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.sim.gre import gre_sim

def cylinder_2d_params():
    '''Returns properties of numerical phantom used in cylinder_2d.'''

    params = {
        'T1': 1.5,
        'T2': 0.8,
        'M0': 5
    }
    return params

def cylinder_2d(dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5,
                params=None):
    '''Base 2d cylinder maps to feed to contrast simulations.'''

    # Grab the numerical parameters
    if params is None:
        params = cylinder_2d_params()

    # Make a bottle
    x = np.linspace(FOV[0][0], FOV[0][1], dims[0])
    y = np.linspace(FOV[1][0], FOV[1][1], dims[1])
    X, Y = np.meshgrid(x, y)
    bottle_idx = np.sqrt(X**2 + Y**2) < radius

    PD = np.zeros(dims).T
    T1s = np.zeros(dims).T
    T2s = np.zeros(dims).T

    PD[bottle_idx] = params['M0']
    T1s[bottle_idx] = params['T1']
    T2s[bottle_idx] = params['T2']

    return(PD, T1s, T2s)


def bssfp_2d_cylinder(TR=6e-3, alpha=np.pi/3, dims=(64, 64),
                      FOV=((-1, 1), (-1, 1)), radius=.5, field_map=None,
                      phase_cyc=0, kspace=False):
    '''Simulates axial bSSFP scan of cylindrical phantom.

    TR -- Repetition time.
    alpha -- Flip angle.
    dims -- Matrix size, (dim_x,dim_y)
    FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
    radius -- Radius of cylinder in arbitrary units.
    field_map -- (dim_x,dim_y) field map. If None, linear gradient in x used.
    phase_cyc -- Phase cycling used in simulated bSSFP acquisition.
    kspace -- Whether or not to return data in kspace or imspace.
    '''

    # Get the base cylinder maps
    PD, T1s, T2s = cylinder_2d(dims=dims, FOV=FOV, radius=radius)

    if field_map is None:
        min_df, max_df = 0, 500
        fx = np.linspace(min_df, max_df, dims[0])
        fy = np.zeros(dims[1])
        field_map, _ = np.meshgrid(fx, fy)

    im = ssfp(T1s, T2s, TR, alpha, field_map, phase_cyc=phase_cyc, M0=PD).T
    # im = gre_sim(T1s,T2s,TR,TR/2,alpha,field_map,phi=phase_cyc,
    #              dphi=phase_cyc,M0=PD,spoil=False,iter=200)
    # im[np.isnan(im)] = 0
    # view(im)

    if kspace:
        return np.fft.fftshift(np.fft.fft2(np.fft.fftshift(
            im), axes=(0, 1)), axes=(0, 1))
    #else...
    return im


def spgr_2d_cylinder(TR=0.3, TE=0.003, alpha=np.pi/3, dims=(64, 64),
                     FOV=((-1, 1), (-1, 1)), radius=.5, field_map=None,
                     kspace=False):
    '''Simulates axial spoiled GRE scan of cylindrical phantom.

    TR -- Repetition time.
    TE -- Echo time.
    alpha -- Flip angle.
    dims -- Matrix size, (dim_x,dim_y)
    FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
    radius -- Radius of cylinder in arbitrary units.
    kspace -- Whether or not to return data in kspace or imspace.
    '''

    # Get the base cylinder maps
    PD, T1s, T2s = cylinder_2d(dims=dims, FOV=FOV, radius=radius)

    # Do the sim
    # im = spoiled_gre(T1s,T2s,TR,TE,alpha,field_map=field_map,M0=PD)
    im = gre_sim(T1s, T2s, TR, TE, alpha, field_map, M0=PD)

    # Hand back what we asked for
    if kspace:
        return np.fft.fftshift(np.fft.fft2(np.fft.fftshift(
            im), axes=(0, 1)), axes=(0, 1))
    #else...
    return im

if __name__ == '__main__':
    pass
