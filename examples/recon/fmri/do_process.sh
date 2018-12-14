
# Create mask - bssfp and gre share the same mask in numerical simulation
3dcalc -a gre.nii.gz -prefix mask.nii -expr "step(a)" -overwrite

# convert from 1/0 behavioral vector file to stim_times style timing file
# -tr 20 refers to the fact that each task was 20 seconds long
make_stim_times.py -files SpT1_timing.txt -prefix stim -tr 20 -nruns 1 -nt 6

# Run the single-subject multiple regression analysis for bSSFP dataset
3dDeconvolve -overwrite \
    -force_TR .75 \
    -input bssfp.nii.gz \
    -polort A \
    -mask mask.nii'[0]' \
    -num_stimts 2 \
    -stim_times 1 stim.01.1D "BLOCK(20,1)" -stim_label 1 "base"  \
    -stim_times 2 stim.02.1D "BLOCK(20,1)" -stim_label 2 "check"  \
    -num_glt 2 \
    -gltsym 'SYM: base' -glt_label 1 base  \
    -gltsym 'SYM: check' -glt_label 2 check  \
    -nocout -tout \
    -bucket deconvolve1_bssfp.nii.gz \
    -errts deconvolve1_bssfp_errts.nii.gz \
    -xjpeg deconvolve1_bssfp_designMatrix.jpg \
    -jobs 2 \
    -GOFORIT 12

# Run the single-subject multiple regression analysis for GRE dataset
3dDeconvolve -overwrite \
    -force_TR .75 \
    -input gre.nii.gz \
    -polort A \
    -mask mask.nii'[0]' \
    -num_stimts 2 \
    -stim_times 1 stim.01.1D "BLOCK(20,1)" -stim_label 1 "base"  \
    -stim_times 2 stim.02.1D "BLOCK(20,1)" -stim_label 2 "check"  \
    -num_glt 2 \
    -gltsym 'SYM: base' -glt_label 1 base  \
    -gltsym 'SYM: check' -glt_label 2 check  \
    -nocout -tout \
    -bucket deconvolve1_gre.nii.gz \
    -errts deconvolve1_gre_errts.nii.gz \
    -xjpeg deconvolve1_gre_designMatrix.jpg \
    -jobs 2 \
    -GOFORIT 12

  # Run the single-subject multiple regression analysis for aFM dataset
  3dDeconvolve -overwrite \
      -force_TR .75 \
      -input qfm.nii.gz \
      -polort A \
      -mask mask.nii'[0]' \
      -num_stimts 2 \
      -stim_times 1 stim.01.1D "BLOCK(20,1)" -stim_label 1 "base"  \
      -stim_times 2 stim.02.1D "BLOCK(20,1)" -stim_label 2 "check"  \
      -num_glt 2 \
      -gltsym 'SYM: base' -glt_label 1 base  \
      -gltsym 'SYM: check' -glt_label 2 check  \
      -nocout -tout \
      -bucket deconvolve1_qfm.nii.gz \
      -errts deconvolve1_qfm_errts.nii.gz \
      -xjpeg deconvolve1_qfm_designMatrix.jpg \
      -jobs 2 \
      -GOFORIT 12
