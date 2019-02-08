
## mr_utils.test_data.phantom.binary_smiley

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/phantom/binary_smiley.py)

```
NAME
    mr_utils.test_data.phantom.binary_smiley - Simple numerical phantom shaped like a smiley face.  Value either 1 or 0.

FUNCTIONS
    binary_smiley(N, radius=0.75)
        Binary smiley face numerical phantom.
        
        N -- Height and width in pixels.
        radius -- Radius of circle used for head.


```


## mr_utils.test_data.phantom.cylinder_2d

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/phantom/cylinder_2d.py)

```
NAME
    mr_utils.test_data.phantom.cylinder_2d - Simple cylindrical phantoms generated with different contrasts.

FUNCTIONS
    bssfp_2d_cylinder(TR=0.006, alpha=1.0471975511965976, dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5, field_map=None, phase_cyc=0, kspace=False)
        Simulates axial bSSFP scan of cylindrical phantom.
        
        TR -- Repetition time.
        alpha -- Flip angle.
        dims -- Matrix size, (dim_x,dim_y)
        FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
        radius -- Radius of cylinder in arbitrary units.
        field_map -- (dim_x,dim_y) field map. If None, linear gradient in x used.
        phase_cyc -- Phase cycling used in simulated bSSFP acquisition.
        kspace -- Whether or not to return data in kspace or imspace.
    
    cylinder_2d(dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5, params=None)
        Base 2d cylinder maps to feed to contrast simulations.
    
    cylinder_2d_params()
        Returns properties of numerical phantom used in cylinder_2d.
    
    spgr_2d_cylinder(TR=0.3, TE=0.003, alpha=1.0471975511965976, dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5, field_map=None, kspace=False)
        Simulates axial spoiled GRE scan of cylindrical phantom.
        
        TR -- Repetition time.
        TE -- Echo time.
        alpha -- Flip angle.
        dims -- Matrix size, (dim_x,dim_y)
        FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
        radius -- Radius of cylinder in arbitrary units.
        kspace -- Whether or not to return data in kspace or imspace.


```


## mr_utils.test_data.phantom.phantom

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/phantom/phantom.py)

```
NAME
    mr_utils.test_data.phantom.phantom

DESCRIPTION
    To Generate phantoms. You can call the following functions with the
    desired phantom shape as input :
    - modified_shepp_logan
    - shepp_logan
    - yu_ye_wang
    You can generate a custom phantom by specifying a list of
    ellipsoid parameters by calling the phantom function.
    Ellipsoid parameters are as follows:
    - A : value inside the ellipsoid
    - a, b, c : axis length of the ellipsoid (in % of the cube shape)
    - x0, y0, z0 : position of the center (in % of the cube shape)
    - phi, theta, psi : Euler angles defining the orientation (in degrees)
    Alternatively, you can generate only one ellipsoid by calling
    the ellipsoid function.
    Exemple
    -------
    To generate a phantom cube of size 32 * 32 * 32 :
    >>> from siddon.phantom import *
    >>> my_phantom = shepp_logan((32, 32, 32))
    >>> assert my_phantom[16, 16, 16] == -0.8
    Notes
    -----
    You can take a look at those links for explanations:
    http://en.wikipedia.org/wiki/Imaging_phantom
    http://en.wikipedia.org/wiki/Ellipsoid
    http://en.wikipedia.org/wiki/Euler_angles
    This module is largely inspired by :
    http://www.mathworks.com/matlabcentral/fileexchange/9416-3d-shepp-logan-phantom
    Author
    ------
    Nicolas Barbey

FUNCTIONS
    modified_shepp_logan(shape, **kargs)
        # define specific functions
    
    phantom(shape, parameters_list, dtype=<class 'numpy.float64'>)
        Generate a cube of given shape using a list of ellipsoid
        parameters.
        Inputs
        ------
        shape: tuple of ints
            Shape of the output cube.
        parameters_list: list of dictionaries
            List of dictionaries with the parameters defining the ellipsoids to
            include in the cube.
        dtype: data-type
            Data type of the output ndarray.
        Output
        ------
        cube: 3-dimensional ndarray
            A 3-dimensional ndarray filled with the specified ellipsoids.
        See Also
        --------
        shepp_logan : Generates the Shepp Logan phantom in any shape.
        modified_shepp_logan : Modified Shepp Logan phantom in any shape.
        yu_ye_wang : The Yu Ye Wang phantom in any shape.
        ellipsoid : Generates a cube filled with an ellipsoid of any shape.
        Notes
        -----
        http://en.wikipedia.org/wiki/Imaging_phantom
    
    shepp_logan(shape, **kargs)
    
    yu_ye_wang(shape, **kargs)

```

