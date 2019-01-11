
## mr_utils.recon.field_map.dual_echo_gre

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/field_map/dual_echo_gre.py)

```
NAME
    mr_utils.recon.field_map.dual_echo_gre

FUNCTIONS
    dual_echo_gre(m1, m2, TE1, TE2)
        Compute wrapped field map from two GRE images at different TEs.
        
        m1 -- GRE image taken with TE = TE1.
        m2 -- GRE image taken with TE = TE2.
        TE1 -- echo time corresponding to m1.
        TE2 -- echo time corresponding to m2.
        
        Returns field map in herz.


```


## mr_utils.recon.field_map.gs_field_map

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/field_map/gs_field_map.py)

```
NAME
    mr_utils.recon.field_map.gs_field_map

FUNCTIONS
    gs_field_map(I0, I1, I2, I3, TR, gs_recon_opts={})
        Use the elliptical signal model to estimate the field map.
        
        I0,I1 -- First phase-cycle pair, separated by 180 degrees.
        I1,I3 -- Second phase-cycle pair, separated by 180 degrees.
        TR -- Repetition time of acquisitons in ms.
        gs_recon_opts -- Options to pass to gs_recon.
        
        Returns wrapped field map in hertz.
        
        Implements field map estimation given in:
            Taylor, Meredith, et al. "MRI Field Mapping using bSSFP Elliptical
            Signal model." Proceedings of the ISMRM Annual Conference (2017).


```

