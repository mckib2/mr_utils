
# RECON
## examples.recon.bssfp.bssfp_difference_constraint

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/bssfp_difference_constraint.py)

```
NAME
    examples.recon.bssfp.bssfp_difference_constraint - Acquire pairs of points that are close together (i.e., dtheta small).

DESCRIPTION
    Given a spectral profile, d(theta), any two points sampled along d(theta), say
    m0 and m1, do not constrain d(theta) to a single possible profile.  Normally,
    we sample at theta=0 and theta=180 degrees and then do a sum of squares for
    optimal SNR banding reduction.  However, if we choose dtheta small, then we can
    constrain d(theta) by two points plus the approximate derivative,
    d/dtheta d(theta), at (theta1 - theta0)/2.
    
    This script attempts to show that this will limit possible realizations of
    d(theta) further than just taking two points 180 degrees apart.  We will also
    try to apply the elliptical signal model with pairs of points taken at small
    theta intervals.


```


## examples.recon.bssfp.bssfp_regression

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/bssfp_regression.py)

```
NAME
    examples.recon.bssfp.bssfp_regression - Find T1, T2, theta given N bSSFP acquisitons.

FUNCTIONS
    M0fun(x, y, T1, T2, theta, TR, alpha)
        Residual for M0 estimation.
    
    fun(x, y, TR, alpha, M0)
        Residual.


```


## examples.recon.bssfp.bssfp_regression_dictionary

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/bssfp_regression_dictionary.py)

```
NAME
    examples.recon.bssfp.bssfp_regression_dictionary - Given two phase cycles, look up T1, T2, theta, M0.


```


## examples.recon.bssfp.merry_param_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/merry_param_mapping.py)

```
NAME
    examples.recon.bssfp.merry_param_mapping - Parameter mapping for numerical phantom using Taylor method.

DESCRIPTION
    Ellipses have 5 degrees of freedom, so you should use 5 or more phase-cycles.
    Use multiples of 4 since we're using GS recon, so use minimum 8.


```


## examples.recon.bssfp.monte_carlo_planet

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/monte_carlo_planet.py)

```
NAME
    examples.recon.bssfp.monte_carlo_planet - Example about how to use PLANET and some if its error characteristics.


```


## examples.recon.bssfp.planet_alpha_sensitivity

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/planet_alpha_sensitivity.py)

```
NAME
    examples.recon.bssfp.planet_alpha_sensitivity - Recreate sensitivity plots from PLANET paper.


```


## examples.recon.bssfp.planet_noisy_case

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/bssfp/planet_noisy_case.py)

```
NAME
    examples.recon.bssfp.planet_noisy_case - Example about how to use PLANET with noisy data.

DESCRIPTION
    So as far as I can tell, this implementation is failing whenever there is any
    noise, no matter how small.  It's probably due to how the ellipse is being
    rotated.


```

