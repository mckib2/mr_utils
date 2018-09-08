# Visualization of frequency as a function of 3d position with arbitrary pulse
# sequence parameters.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_grid(xparams,yparams,zparams):
    x = np.linspace(*xparams)
    y = np.linspace(*yparams)
    z = np.linspace(*zparams)
    X,Y,Z = np.meshgrid(x,y,z)
    return(X,Y,Z)

def apply_gradients(XYZ,Gi,B0=3,gamma=42.58*2*np.pi*1e6):
    Gi = np.array(Gi)
    XYZ = np.array(XYZ)
    W0 = gamma*(B0*np.ones(XYZ[0].shape) + Gi.dot(XYZ.transpose(1,2,0,3)))
    return(W0)

def excite(XYZ,W,BW,B0=3,gamma=42.58*2*np.pi*1e6):
    # This is basically masking all frequencies except those excited
    w0 = B0*gamma
    mask = np.logical_and(W >= (w0 - BW/2),W <= (w0 + BW/2))
    W0 = W*mask
    X,Y,Z = [ mask*U for U in XYZ ]
    return(X,Y,Z,W0)

def show_slices(XYZ,W):
    fig = plt.figure()

    for ii in range(W.shape[-1]):
        ax = fig.gca(projection='3d')
        ax.plot_surface(*[ A[:,:,ii] for A in XYZ[:-1] ],W[:,:,ii])
    plt.show()

if __name__ == '__main__':

    # Create a grid
    lims = .005
    num_x = 4
    num_y = 8
    num_slices = 5
    X,Y,Z = create_grid((-lims,lims,num_x),(-lims,lims,num_y),(-lims,lims,num_slices))

    # Initialize omegas to random frequencies
    a,b = -1.e6,1e6 # Hz
    W = (b - a)*np.random.random(X.shape) + a
    # show_slices((X,Y,Z),W)

    # Enter main magnetic field
    gamma = 42.58*2*np.pi*1e6 # Hz/T
    B0 = 3 # T
    W = np.ones(X.shape)*gamma*B0
    # show_slices((X,Y,Z),W)

    # Slice select gradient
    Gx,Gy,Gz = 0,0,20e-3 # Hz/T
    W = apply_gradients((X,Y,Z),(Gx,Gy,Gz))
    show_slices((X,Y,Z),W)

    # Excitation
    BW = 1000 # Hz
    X,Y,Z,W = excite((X,Y,Z),W,BW)
    show_slices((X,Y,Z),W)

    # Phase Encode
    Gx,Gy,Gz = 0,20e-3,0 # Hz/T
    W = apply_gradients((X,Y,Z),(Gx,Gy,Gz))
    show_slices((X,Y,Z),W)

    # Frequency Encode
    Gx,Gy,Gz = 10e-3,20e-3,0 # Hz/T
    W = apply_gradients((X,Y,Z),(Gx,Gy,Gz))
    show_slices((X,Y,Z),W)
