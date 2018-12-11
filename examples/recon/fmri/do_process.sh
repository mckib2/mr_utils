
# Create mask
3dcalc -a gre.nii.gz -prefix bssfp_mask.nii -expr "step(a)"

# convert from 1/0 behavioral vector file to stim_times style timing file
# -tr 10 refers to the fact that each task was 20 seconds long
make_stim_times.py -files SpT1_timing.txt -prefix stim -tr 20 -nruns 1 -nt 6

# Run the single-subject multiple regression analysis
3dDeconvolve -input bssfp.nii.gz \
    -polort A \
    -mask bssfp_mask.nii \
    -force_TR 0.005 \
    -num_stimts 2 \
    -stim_times 1 stim.01.1D "BLOCK(20,1)" -stim_label 7 "base"  \
    -stim_times 2 stim.02.1D "BLOCK(20,1)" -stim_label 8 "check"  \
    -censor 'motion_censor_vector_censor.1D[0]' \
    -num_glt 2 \
    -gltsym 'SYM: base' -glt_label 1  base  \
    -gltsym 'SYM: check' -glt_label 2  check  \
    -nocout -tout \
    -bucket deconvolve1.nii.gz \
    -errts deconvolve1_errts.nii.gz \
    -xjpeg deconvolve1_designMatrix.jpg \
    -jobs 2 \
    -GOFORIT 12
