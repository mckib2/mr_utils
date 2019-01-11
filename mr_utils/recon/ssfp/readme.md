
## mr_utils.recon.ssfp.dixon

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/dixon.py)

```
NAME
    mr_utils.recon.ssfp.dixon

FUNCTIONS
    dixon_2pt(IP, OP)
        Naive two-point Dixon method of fat/water separation.
        
        IP -- In-phase image (corresponding to 0).
        OP -- Out-of-phase image (corresponding to pi).
        
        Returns water image, W, and fat image, F.
        
        "[This implementation] ignores additional image weighting from T2*
        relaxation, diffusion, and flow and from other phase shifts that could
        arise from hardware group delays, eddy currents, and B1 receive-field
        nonuniformity. We have also ignored the water-fat chemical shift
        separation in both the slice and readout directions"
        
        Implements method described in:
            Dixon, W. T. (1984). Simple proton spectroscopic imaging. Radiology,
        Also equations [17.52] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_2pt_mag(IP, OP)
        Solution to two-point Dixon method using magnitude of images.
        
        IP -- In-phase image (corresponding to 0).
        OP -- Out-of-phase image (corresponding to pi).
        
        Returns water image, abs(W), and fat image, abs(F).
        
        Implements equations [17.53-54] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_3pt(IP, OP1, OP2, use_2pi=True, method='glover')
        Three point Dixon method of fat/water separation.
        
        IP -- In-phase image (corresponding to 0).
        OP1 -- Out-of-phase image (corresponding to pi).
        OP2 -- Out-of-phase image (corresponding to -pi or 2*pi).
        use_2pi -- Use 2*pi for OP2 instead of -pi.
        method -- Method to use to determine pc, see dixon_pc().
        
        Returns water image, W, fat image, F, and B0 image.
        
        "The phase difference between the two opposed-phase images is due
        to B0 inhomogeneity, and they are used to compute phi. The phi map is used
        to remove the B0 inhomogeneity phase shift from one of the opposed-phase
        images and thereby determine the dominant species for each pixel (i.e.,
        whether W > F, or vice versa)."
        
        Implements method described:
            Glover, G. H., & Schneider, E. (1991). Three‐point Dixon technique for
            true water/fat decomposition with B0 inhomogeneity correction. Magnetic
            resonance in medicine, 18(2), 371-383.
        
        Also implements equations [17.71] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_3pt_dpe(I0, I1, I2, theta)
        Three point Dixon using direct phase encoding (DPE).
        
        Note that theta_0 + theta should not be a multiple of pi!
        
        Implements equations [17.83-84] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_3pt_eam(I0, I1, I2, method='glover')
        Three point Dixon including echo amplitude modulation (EAM).
        
        I0 -- In-phase image (corresponding to phi_0 phase).
        I1 -- Out-of-phase image (corresponding to phi_0 + phi).
        I2 -- Out-of-phase image (corresponding to phi_0 + 2*phi).
        method -- Method to use to determine pc, see dixon_pc().
        
        Returns water image, W, fat image, F, and A, the susceptibility dephasing
        map.
        
        "...under our assumptions, ignoring amplitude effects simply results in a
        multiplicative error in both water and fat components. This error is
        usually not serious and can be ignored...there is a SNR penalty for the
        amplitude correction, and it is best avoided unless there is a specific
        need to compute A for the application of interest."
        
        Implements equations [17.78] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_extended_2pt(IP, OP, method='glover')
        Extended two-point Dixon method for fat/water separation.
        
        IP -- In-phase image (corresponding to 0).
        OP -- Out-of-phase image (corresponding to pi).
        method -- Method to use to determine pc, see dixon_pc().
        
        Returns water image, abs(W), and fat image, abs(F).
        
        Extended 2PD attempts to address the B0 homogeneity problem by using a
        generalized pc.
        
        Implements equations [17.63] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_pc(IP, OP, method='vanilla')
        Methods to determine pc, fat/water fraction within a voxel.
        
        method:
            'vanilla': sign of W - F.
            'glover': maintain continuous image appearance by using cont. p value.
            'chen': alternative that performs 'glover' and then discretizes.
        
        'glover' is implementation of eq [17.62], 'chen' is implementation of eq
        [17.64-65], 'vanilla' is eq [17.54] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.


```


## mr_utils.recon.ssfp.gs_recon

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/gs_recon.py)

```
NAME
    mr_utils.recon.ssfp.gs_recon

FUNCTIONS
    complex_sum(I1, I2, I3, I4)
    
    compute_Iw(I0, I1, Id, patch_size=(5, 5), mode='constant', isophase=3.141592653589793)
        Computes weighted sum of image pair (I0,I1).
        
        I0 -- 1st of pair of diagonal images (relative phase cycle of 0).
        I1 -- 2nd of pair of diagonal images (relative phase cycle of 180 deg).
        Id -- result of regularized direct solution.
        patch_size -- size of patches in pixels (x,y).
        mode -- mode of numpy.pad. Probably choose 'constant' or 'edge'.
        isophase -- Only neighbours with max phase difference isophase contribute.
        
        Image pair (I0,I1) are phase cycled bSSFP images that are different by
        180 degrees.  Id is the image given by the direct method (Equation [13])
        after regularization by the complex sum.  This function solves for the
        weights by regional differential energy minimization.  The 'regional'
        part means that the image is split into patches of size patch_size with
        edge boundary conditions (pads with the edge values given by mode option).
        The weighted sum of the image pair is returned.
        
        The isophase does not appear in the paper, but appears in Hoff's MATLAB
        code.  It appears that we only want to consider pixels in the patch that
        have similar tissue properties - in other words, have similar phase.  The
        default isophase is pi as in Hoff's implementation.
        
        This function implements Equations [14,18], or steps 4--5 from Fig. 2 in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    get_max_magnitudes(I1, I2, I3, I4)
        Find maximum magnitudes for each pixel over all four input images.
    
    get_max_magnitudes_for_loop(I1, I2, I3, I4)
        Find maximum magnitudes for each pixel over all four input images.
        
        This one loops over each pixel as verification for get_max_magnitudes().
    
    gs_recon(I1, I2, I3, I4, isophase=3.141592653589793, second_pass=True)
        Full 2D Geometric Solution method following Xiang and Hoff's 2014 paper.
        
        I1,I3 -- 1st diagonal pair of images (offset 180 deg).
        I2,I4 -- 2nd diagonal pair of images (offset 180 deg).
        isophase -- Only neighbours with isophase max phase difference contribute.
        second_pass -- Compute the second pass solution, increasing SNR by sqrt(2).
        
        Implements algorithm shown in Fig 2 of
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    gs_recon3d(I1, I2, I3, I4, slice_axis=-1, isophase=3.141592653589793)
        Full 3D Geometric Solution method following Xiang and Hoff's 2014 paper.
        
        I1--I4 -- Phase-cycled images.
        slice_axis -- Slice dimension, default is the last dimension.
        For more info, see mr_utils.recon.ssfp.gs_recon.
    
    gs_recon_for_loop(I1, I2, I3, I4)
    
    mask_isophase(numerator_patches, patch_size, isophase)
        Generate mask that chooses patch pixels that satisfy isophase.
        
        numerator_patches -- Numerator patches from second pass solution.
        patch_size -- size of patches in pixels (x,y).
        isophase -- Only neighbours with isophase max phase difference contribute.
        
        Output mask, same size as numerator_patches, to be applied to
        numerator_patches and den_patches before summation.


```


## mr_utils.recon.ssfp.multiphase

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/multiphase.py)

```
NAME
    mr_utils.recon.ssfp.multiphase

FUNCTIONS
    multiphase(kspace)
        Acquire two phase-cycled images in one Cartesian acquisiton.
        
        The idea is to acquire kspace with even lines having phase-cycle \phi_0 and
        and odd lines having phase-cycle \phi_1.  Then split the lines up into
        two R=2 undersampled images and use parallel imaging reconstruction to
        recover the two separate phase-cycled images.
        
        kspace -- Even lines phase \phi_0, odd lines phase \phi_1.


```

