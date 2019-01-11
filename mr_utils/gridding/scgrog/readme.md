
# GRIDDING
## mr_utils.gridding.scgrog.get_gx_gy

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gridding/scgrog/get_gx_gy.py)

```
NAME
    mr_utils.gridding.scgrog.get_gx_gy

FUNCTIONS
    get_gx_gy(kspace, traj=None, kxs=None, kys=None, cartdims=None)
        Compute Self Calibrating GRAPPA Gx and Gy operators.


```


## mr_utils.gridding.scgrog.scgrog

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gridding/scgrog/scgrog.py)

```
NAME
    mr_utils.gridding.scgrog.scgrog

FUNCTIONS
    grog_interp(kspace, Gx, Gy, traj, cartdims)
        Moves radial k-space points onto a cartesian grid via the GROG method.
        
        kspace    -- A 3D (sx,sor,soc) slice of k-space
        Gx,Gy     -- The unit horizontal and vertical cartesian GRAPPA kernels
        trak      -- k-space trajectory
        cartdims  -- (nrows,ncols), size of Cartesian grid
    
    scgrog(kspace, traj, Gx, Gy, cartdims=None)


```

