
## mr_utils.sim.traj.cartesian

[Source](../master/mr_utils/sim/traj/cartesian.py)

```
NAME
    mr_utils.sim.traj.cartesian

FUNCTIONS
    cartesian_gaussian(shape, undersample=(0.5, 0.5), reflines=20)
    
    cartesian_pe(shape, undersample=0.5, reflines=20)


```


## mr_utils.sim.traj.radial

[Source](../master/mr_utils/sim/traj/radial.py)

```
NAME
    mr_utils.sim.traj.radial

FUNCTIONS
    radial(shape, num_spokes, theta=None, skinny=True, extend=False)
        Create 2d binary radial sampling pattern.
        
        shape -- x,y dimensions of sampling pattern.
        num_spokes -- Number of spokes to simulate.
        theta -- Angle between spokes (rad).
        skinny -- Garuantee 1px spoke width.
        extend -- Extend spokes to the edge of array.
        
        If theta=None, use golden angle. If skinny=True, edges of spokes with large
        slope may be curved. If extend=False, spokes confined in a circle.
    
    radial_golden_ratio_meshgrid(X, Y, num_spokes)
        Create 2d binary golden angle radial sampling pattern.
        
        X,Y -- Meshgrid.
        num_spokes -- Number of spokes to simulate.
        
        Issues:
            For steep slopes, the spokes don't make it all the way to the edge of
            the image and they curve (from the skeletonize)...


```

