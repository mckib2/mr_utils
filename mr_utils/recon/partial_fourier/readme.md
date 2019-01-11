
## mr_utils.recon.partial_fourier.partial_fourier_pocs

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/partial_fourier/partial_fourier_pocs.py)

```
NAME
    mr_utils.recon.partial_fourier.partial_fourier_pocs - # Python port of Gadgetron's 2D partial_fourier_POCS

FUNCTIONS
    apply_kspace_filter_ROE1(data, FRO, FE1)
    
    compute_2d_filter(fx, fy)
    
    generate_symmetric_filter(length, filterType, sigma=1.5, width=15)
    
    generate_symmetric_filter_ref(length, start, end)
    
    partial_fourier_pocs(kspace, startRO, endRO, startE1, endE1, transit_band_RO=0, transit_band_E1=0, iter=10, thres=0.01)
        # kspace: input kspace [RO E1 E2 ...]
        # 2D POCS is performed
        # startRO, endRO, startE1, endE1: acquired kspace range
        # transit_band_RO/E1: transition band width in pixel for RO/E1
        # iter: number of maximal iterations for POCS
        # thres: iteration threshold
    
    partial_fourier_reset_kspace(src, dst, startRO, endRO, startE1, endE1)

```

