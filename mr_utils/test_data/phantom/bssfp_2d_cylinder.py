import numpy as np
from mr_utils.sim.ssfp import ssfp_mat
from mr_utils import view

def bssfp_2d_cylinder_params():
    '''Returns properties of numerical phantom used in bssfp_cylinder.'''

    params = {
        'T1': 1.5,
        'T2': 0.8,
        'M0': 5
    }
    return(params)

def bssfp_2d_cylinder(TR=6e-3,alpha=np.pi/3,dims=(64,64),FOV=((-1,1),(-1,1)),radius=.5,field_map=None,phase_cyc=0):
    '''Simulates axial bSSFP scan of cylindrical phantom.

    TR -- Repetition time.
    alpha -- Flip angle.
    dims -- Matrix size, (dim_x,dim_y)
    FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
    radius -- Radius of cylinder in arbitrary units.
    field_map -- (dim_x,dim_y) field map. If None, linear gradient in x used.
    '''

    # Grab the numerical parameters
    params = bssfp_2d_cylinder_params()

    # Bottle
    x = np.linspace(FOV[0][0],FOV[0][1],dims[0])
    y = np.linspace(FOV[1][0],FOV[1][1],dims[1])
    X,Y = np.meshgrid(x,y)
    bottle_idx = np.sqrt(X**2 + Y**2) < radius

    PD = np.random.normal(0,0.1,dims) # this controls noise level
    T1s = np.zeros(dims)
    T2s = np.zeros(dims)

    PD[bottle_idx] = params['M0']
    T1s[bottle_idx] = params['T1']
    T2s[bottle_idx] = params['T2']

    if field_map is None:
        min_df,max_df = 0,500
        fx = np.linspace(min_df,max_df,dims[0])
        fy = np.zeros(dims[1])
        field_map,_ = np.meshgrid(fx,fy)

    im = ssfp_mat(T1s,T2s,TR,alpha,field_map,phase_cyc=phase_cyc,M0=PD)
    # view(im)
    return(im)

if __name__ == '__main__':
    pass
