
## mr_utils.recon.reordering.bart

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/bart.py)

```
NAME
    mr_utils.recon.reordering.bart

```


## mr_utils.recon.reordering.lcurve

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/lcurve.py)

```
NAME
    mr_utils.recon.reordering.lcurve

FUNCTIONS
    lcurve(norm0, norm1)


```


## mr_utils.recon.reordering.patch_reordering

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/patch_reordering.py)

```
NAME
    mr_utils.recon.reordering.patch_reordering

FUNCTIONS
    get_patches(imspace, patch_size)


```


## mr_utils.recon.reordering.rudin_osher_fatemi

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/rudin_osher_fatemi.py)

```
NAME
    mr_utils.recon.reordering.rudin_osher_fatemi

FUNCTIONS
    check_stability(dt, h, c=300000000.0)
        Check stepsize restriction, imposed for for stability.
    
    getbounds(ii, jj, u0)
    
    minmod(a, b)
        Flux limiter to make FD solutions total variation diminishing.
    
    update_all_for_loop(u0, dt, h, sigma, niters)


```


## mr_utils.recon.reordering.scr_reordering_adluru

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/scr_reordering_adluru.py)

```
NAME
    mr_utils.recon.reordering.scr_reordering_adluru

FUNCTIONS
    TVG(out_img, beta_sqrd)
    
    TVG_re_order(out_img, beta_sqrd, sort_order_real_x, sort_order_real_y)
    
    intshft(m, sh)
        Shift image m by coordinates specified by sh
    
    scr_reordering_adluru(kspace, mask, prior=None, alpha0=1, alpha1=0.002, beta2=1e-08, reorder=True, reorder_every_iter=False, enforce_consistency=False, niters=5000)
        Reconstruct undersampled data with spatial TV constraint and reordering.
        
        kspace -- Undersampled k-space data
        mask -- Undersampling mask
        prior -- Prior image estimate, what to base reordering on
        alpha0 -- Weight of the fidelity term in cost function
        alpha1 -- Weight of the TV term, regularization parameter
        beta2 -- beta squared, small constant to keep sqrt defined
        reorder -- Whether or not to reorder data
        reorder_every_iter -- Reorder each iteration based on current estimate
        enforce_consistency -- Fill in known values of kspace each iteration
        niters -- Number of iterations
        
        Ref: G.Adluru, E.V.R. DiBella. "Reordering for improved constrained
        reconstruction from undersampled k-space data". International Journal of
        Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008.
        doi:10.1155/2008/341684.
    
    sort_real_imag_parts_space(full_data_recon_complex)
        Determines the sort order for real and imag components.
    
    time(...)
        time() -> floating point number
        
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.


```


## mr_utils.recon.reordering.sort2d

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/sort2d.py)

```
NAME
    mr_utils.recon.reordering.sort2d

FUNCTIONS
    sort2d(A)
    
    sort2d_loop(A)
        An efficient selection sorting algorithm for two-dimensional arrays.
        
        Implementation of algorithm from:
            Zhou, M., & Wang, H. (2010, December). An efficient selection sorting
            algorithm for two-dimensional arrays. In Genetic and Evolutionary
            Computing (ICGEC), 2010 Fourth International Conference on
            (pp. 853-855). IEEE.


```


## mr_utils.recon.reordering.tsp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/tsp.py)

```
NAME
    mr_utils.recon.reordering.tsp

FUNCTIONS
    create_distance_callback(dist_matrix)
        # Distance callback
    
    generate_orderings(im=None)
    
    get_dist_matrix()
    
    get_slice(lpf=True, lpf_factor=6)
    
    get_time_series(im, x=100, y=100, real_part=True, patch=False, patch_pad=(1, 1))
    
    normalize_time_series(time_series0)
    
    ortools_tsp_solver()


```

