
## mr_utils.sim.traj.cartesian

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/traj/cartesian.py)

```
NAME
    mr_utils.sim.traj.cartesian - Create sampling patterns for Cartesian k-space trajectories.

FUNCTIONS
    cartesian_gaussian(shape, undersample=(0.5, 0.5), reflines=20)
        Undersample in Gaussian pattern.
    
    cartesian_pe(shape, undersample=0.5, reflines=20)
        Randomly collect Cartesian phase encodes (lines).
        
        shape -- Shape of the image to be sampled.
        undersample -- Undersampling factor (0 < undersample <= 1).
        reflines -- Number of lines in the center to collect regardless.


```


## mr_utils.sim.traj.radial

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/traj/radial.py)

```
NAME
    mr_utils.sim.traj.radial - Generate radial sampling masks.

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

