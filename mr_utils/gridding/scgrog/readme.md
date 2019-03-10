
# GRIDDING
## mr_utils.gridding.scgrog.get_gx_gy

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gridding/scgrog/get_gx_gy.py)

```
NAME
    mr_utils.gridding.scgrog.get_gx_gy - Self calibrating GROG GRAPPA kernels.

DESCRIPTION
    Based on the MATLAB implementation found here:
        https://github.com/edibella/Reconstruction/blob/master/%2BGROG/get_Gx_Gy.m

FUNCTIONS
    get_gx_gy(kspace, traj=None, kxs=None, kys=None, cartdims=None)
        Compute Self Calibrating GRAPPA Gx and Gy operators.


```


## mr_utils.gridding.scgrog.scgrog

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gridding/scgrog/scgrog.py)

```
NAME
    mr_utils.gridding.scgrog.scgrog - Self calibrating GROG implementation.

DESCRIPTION
    Based on the MATLAB GROG implementation found here:
        https://github.com/edibella/Reconstruction

FUNCTIONS
    fracpowers(idx, Gx, Gy, dkxs, dkys)
        Wrapper function to use during parallelization.
    
    grog_interp(kspace, Gx, Gy, traj, cartdims)
        Moves radial k-space points onto a cartesian grid via the GROG method.
        
        kspace -- A 3D (sx,sor,soc) slice of k-space
        Gx,Gy -- The unit horizontal and vertical cartesian GRAPPA kernels
        traj -- k-space trajectory
        cartdims -- (nrows,ncols), size of Cartesian grid
    
    scgrog(kspace, traj, Gx, Gy, cartdims=None)
        Self calibrating GROG interpolation.
        
        kspace -- A 4D (sx,sor,nof,soc) matrix of complex k-space data.
        traj -- k-space trajectory.
        Gx,Gy -- The unit horizontal and vertical cartesian GRAPPA kernels.
        cartdims -- Size of Cartesian grid.
        
        If cartdims=None, we'll guess the Cartesian dimensions are
        (kspace.shape[0], kspace.shape[0], kspace.shape[2], kspace.shape[3]).


```

