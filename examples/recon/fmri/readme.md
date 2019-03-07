
## examples.recon.fmri.transition_band_bssfp

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/recon/fmri/transition_band_bssfp.py)

```
NAME
    examples.recon.fmri.transition_band_bssfp - Demonstration of bSSFP fMRI using field maps.

FUNCTIONS
    bssfp_acq(T1s, T2s, PD, field_map, TR=0.005, alpha=0.17453292519943295, phase_cyc=0)
        Wrapper to simulate bSSFP acquisition.
    
    gre_acq(T1s, T2s, PD, field_map, TR, TE, alpha=1.5707963267948966)
        Wrapper to simulate spoled GRE acquisition.
    
    hrf(times0)
        Return values for HRF at given times
        
        From:
            http://www.jarrodmillman.com/rcsds/lectures/convolution_background.html

```

