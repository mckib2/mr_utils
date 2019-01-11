
## mr_utils.sim.ssfp.param_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/param_mapping.py)

```
NAME
    mr_utils.sim.ssfp.param_mapping

FUNCTIONS
    gen_dictionary(t1t2alpha, TR, TE)
    
    ssfp(T1, T2, alpha, TR, TE, fs, dphi, phi=0, M0=1)


```


## mr_utils.sim.ssfp.quantitative_field_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/quantitative_field_mapping.py)

```
NAME
    mr_utils.sim.ssfp.quantitative_field_mapping

FUNCTIONS
    get_df_responses(T1, T2, PD, TR, alpha, phase_cyc, dfs)
        Simulate bSSFP response across all possible off-resonances.
        
        T1 -- scalar T1 longitudinal recovery value in seconds.
        T2 -- scalar T2 transverse decay value in seconds.
        PD -- scalar proton density value scaled the same as acquisiton.
        TR -- Repetition time in seconds.
        alpha -- Flip angle in radians.
        phase_cyc -- RF phase cycling in radians.
        dfs -- Off-resonance values to simulate over.
    
    quantitative_fm(Mxys, dfs, T1s, T2s, PDs, TR, alpha, phase_cyc, mask=None)
        Find field map given quantitative maps.
    
    quantitative_fm_scalar(Mxy, dfs, T1, T2, PD, TR, alpha, phase_cyc)
        For scalar T1,T2,PD


```


## mr_utils.sim.ssfp.ssfp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/ssfp.py)

```
NAME
    mr_utils.sim.ssfp.ssfp

FUNCTIONS
    elliptical_params(T1, T2, TR, alpha, M0=1)
        Return ellipse parameters M,a,b.
        
        T1 -- longitudinal exponential decay time constant.
        T2 -- transverse exponential decay time constant.
        TR -- repetition time.
        alpha -- flip angle.
        
        Outputs are the parameters of ellipse an ellipse, (M,a,b).  These
        parameters do not depend on theta.
        
        Implementation of equations [3-5] in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    get_bssfp_phase(TR, field_map, delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)
        Additional bSSFP phase factors.
        
        TR -- repetition time.
        field_map -- off-resonance map (Hz).
        delta_cs -- chemical shift of species w.r.t. the water peak (Hz).
        phi_rf -- RF phase offset, related to the combination of Tx/Rx phases (rad).
        phi_edd -- phase errors due to eddy current effects (rad).
        phi_drift -- phase errors due to B0 drift (rad).
        
        This is exp(-i phi) from end of p. 930 in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
        
        In Hoff's paper the equation is not explicitly given for phi, so we
        implement equation [5] that gives more detailed terms, found in
            Shcherbakova, Yulia, et al. "PLANET: An ellipse fitting approach for
            simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
            free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.
    
    get_cart_elliptical_params(M, a, b)
        Get parameters needed for cartesian representation of ellipse.
    
    get_center_of_mass(M, a, b)
        Give center of mass a function of ellipse parameters.
    
    get_center_of_mass_nmr(T1, T2, TR, alpha, M0=1)
        Give center of mass as a function of NMR parameters.
    
    get_complex_cross_point(I1, I2, I3, I4)
        Find the intersection of two straight lines connecting diagonal pairs.
        
        (xi,yi) are the real and imaginary parts of complex valued pixels in four
        bSSFP images denoted Ii and acquired with phase cycling dtheta = (i-1)*pi/2
        with 0 < i <= 4.
        
        This is Equation [13] from:
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    get_cross_point(I1, I2, I3, I4)
        Find the intersection of two straight lines connecting diagonal pairs.
        
        (xi,yi) are the real and imaginary parts of complex valued pixels in four
        bSSFP images denoted Ii and acquired with phase cycling dtheta = (i-1)*pi/2
        with 0 < i <= 4.
        
        This are Equations [11-12] from:
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
        
        There is  a typo in the paper for equation [12] fixed in this
        implementation.  The first term of the numerator should have (y2 - y4)
        instead of (x2 - y4) as written.
    
    get_geo_center(M, a, b)
        Get geometric center of ellipse.
    
    get_theta(TR, field_map, phase_cyc=0)
        Get theta, spin phase per repetition time, given off-resonance.
        
        Equation for theta=2*pi*df*TR is in Appendix A of
            Hargreaves, Brian A., et al. "Characterization and reduction of the
            transient response in steady‐state MR imaging." Magnetic Resonance in
            Medicine: An Official Journal of the International Society for Magnetic
            Resonance in Medicine 46.1 (2001): 149-158.
    
    make_cart_ellipse(xc, yc, A, B, num_t=100)
        Make a cartesian ellipse, return x,y coordinates for plotting.
    
    spectrum(T1, T2, TR, alpha)
        Generate an entire period of the bSSFP signal profile.
    
    ssfp(T1, T2, TR, alpha, field_map, phase_cyc=0, M0=1)
        SSFP transverse signal right after RF pulse.
        
        T1 -- longitudinal exponential decay time constant.
        T2 -- transverse exponential decay time constant.
        TR -- repetition time.
        alpha -- flip angle.
        field_map -- B0 field map.
        M0 -- proton density.
        
        Implementation of equations [1-2] in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    ssfp_from_ellipse(M, a, b, TR, field_map, phase_cyc=0)
        Simulate banding artifacts given elliptical signal params and field map.
    
    ssfp_old(T1, T2, TR, alpha, field_map, phase_cyc=0, M0=1)
        Legacy SSFP sim code.  Try using current SSFP function.


```


## mr_utils.sim.ssfp.ssfp_dictionary

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/ssfp_dictionary.py)

```
NAME
    mr_utils.sim.ssfp.ssfp_dictionary

FUNCTIONS
    find_atom(sig, D, keys)
        Find params of dictionary atom closest to observed signal profile.
    
    get_keys(T1s, T2s, alphas)
        Generate matrix of params [T1,T2,alpha] to generate a dictionary.
        
        T1,T2 are chosen to be feasible, i.e., T1 >= T2.
    
    ssfp_dictionary(T1s, T2s, TR, alphas, df)
        Generate a dicionary of bSSFP profiles given parameters.
        
        T1s -- (1D) all T1 decay constant values to simulate.
        T2s -- (1D) all T2 decay constant values to simulate.
        TR -- repetition time for bSSFP simulation.
        alphas -- (1D) all flip angle values to simulate.
        df -- (1D) off-resonance frequencies over which to simulate.
        
        T1s,T2s,alphas should all be 1D arrays.  All feasible combinations will be
        simulated (i.e., where T1 >= T2).  The dictionary and keys will be returned.
        Each dictionary column is the simulation over frequencies df.  The keys are
        a list of tuples: (T1,T2,alpha).
    
    ssfp_dictionary_for_loop(T1s, T2s, TR, alphas, df)
        Verification for ssfp_dictionary generation.


```

