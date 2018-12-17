# Tell me where we need to be
DIR="path/to/work/directory"

# Log out the output
LOG="path/to/log.txt"

# For each subject, do the thing!
# for subject in $DIR/s*
for subject in $DIR/s*
do
  # Convert structural dicoms to nifti
  to3d -session ${subject} -prefix struct.nii ${subject}/data/structural >> ${LOG}

  # Convert functional dicoms to nifti
  to3d -session ${subject} -prefix gre_func.nii -time:zt 40 180 2.500sec alt+z ${subject}/data/GRE* >> ${LOG}
  # to3d -session ${subject} -prefix ffm_func.nii -time:zt 40 180 2.500sec alt+z ${subject}/data/FFM* >> ${LOG} # already done!

  # Do a time shift...
  # 3dTshift -prefix <output.nii> <input.nii>
  (cd $subject && 3dTshift -prefix gre_func_shifted.nii gre_func.nii)
  (cd $subject && 3dTshift -prefix ffm_func_shifted.nii ffm_func.nii)

  # Do motion detection - choose center brick as reference
  (cd $subject && 3dvolreg -base gre_func_shifted.nii'[90]' -prefix gre_func_shifted_volreg.nii -1Dfile motion_gre.txt gre_func_shifted.nii >> ${LOG})
  (cd $subject && 3dvolreg -base ffm_func_shifted.nii'[90]' -prefix ffm_func_shifted_volreg.nii -1Dfile motion_ffm.txt ffm_func_shifted.nii >> ${LOG})

  # We want just one motion.txt file, so let's make it
  (cd $subject && cat motion_gre.txt motion_ffm.txt >> motion.txt)

  # We need to match both functional (need 3dvolreg) and struct (need 3dWarp)
  (cd $subject && 3dvolreg -base gre_func_shifted.nii'[0]' -prefix ffm_func_shifted_volreg_aligned.nii ffm_func_shifted_volreg.nii >> ${LOG})
  (cd $subject && 3dWarp -oblique_parent gre_func_shifted_volreg.nii -prefix struct_rotated.nii struct.nii >> ${LOG})

  # create the censor file based on motion events. Requires motion.txt output from 3dvolreg
  (cd $subject && 1d_tool.py -infile motion.txt -set_nruns 1 -show_censor_count -censor_prev_TR -censor_motion 0.6 motion_censor_vector >> ${LOG})

  # create a skull-stripped structural, resample it to functional dimensions, binarize
  (cd $subject && 3dSkullStrip -input struct_rotated.nii -o_ply anat_brain.nii >> $LOG)
  (cd $subject && 3dfractionize -template func_4_shifted_volreg.nii -input anat_brain.nii -prefix struct_resamp.nii >> $LOG)
  (cd $subject && 3dcalc -a struct_resamp.nii -prefix struct_mask.nii -expr "step(a)" >> $LOG)

  # Format timing file
  ./make_stim.py -f $(ls ${subject}/timing* | head -3 | tr '\n' ' ') -o ${subject}/SpT1_timing_gre.txt
  ./make_stim.py -f $(ls ${subject}/timing* | tail -3 | tr '\n' ' ') -o ${subject}/SpT1_timing_ffm.txt

  # convert from 1/0 behavioral vector file to stim_times style timing file
  # -tr 10 refers to the fact that each task was 10 seconds long
  (cd $subject && make_stim_times.py -files SpT1_timing_4.txt -prefix stim_gre -tr 10 -nruns 1 -nt 45 >> $LOG)
  (cd $subject && make_stim_times.py -files SpT1_timing_10.txt -prefix stim_ffm -tr 10 -nruns 1 -nt 45 >> $LOG)

  # Combine stim files for each run into 1 file for each condition
  (cd $subject && cat stim_4.01.1D stim_10.01.1D >> checks.1D)
  (cd $subject && cat stim_4.02.1D stim_10.02.1D >> fixation.1D)

  # run the single-subject multiple regression analysis
  # Correct for motion, let AFNI choose the polynomial regressors, and do
  # GLTs for checks and fixation conditions.
  (cd $subject && 3dDeconvolve -input func_4_shifted_volreg.nii func_10_shifted_volreg_aligned.nii \
      -polort A \
      -mask struct_mask.nii \
      -num_stimts 8 \
      -stim_file 1 motion.txt'[0]' -stim_base 1 -stim_label 1 roll \
      -stim_file 2 motion.txt'[1]' -stim_base 2 -stim_label 2 pitch \
      -stim_file 3 motion.txt'[2]' -stim_base 3 -stim_label 3 yaw \
      -stim_file 4 motion.txt'[3]' -stim_base 4 -stim_label 4 dS \
      -stim_file 5 motion.txt'[4]' -stim_base 5 -stim_label 5 dL \
      -stim_file 6 motion.txt'[5]' -stim_base 6 -stim_label 6 dP \
      -stim_times 7 checks.1D "BLOCK(10,1)" -stim_label 7 "checks"  \
      -stim_times 8 fixation.1D "BLOCK(10,1)" -stim_label 8 "fixation"  \
      -censor 'motion_censor_vector_censor.1D[0]' \
      -num_glt 2 \
      -gltsym 'SYM: checks'   -glt_label 1  checks  \
      -gltsym 'SYM: fixation'    -glt_label 2  fixation  \
      -nocout -tout \
      -bucket deconvolve1.nii.gz \
      -errts deconvolve1_errts.nii.gz \
      -xjpeg deconvolve1_designMatrix.jpg \
      -jobs 2 \
      -GOFORIT 12 >> $LOG)

    # Blur before ANTS
    (cd $subject && 3dmerge -prefix deconvolve1_blur8.nii.gz -1blur_fwhm 8.0 -doall deconvolve1.nii.gz >> ${LOG})
    (cd $subject && 3dmerge -prefix deconvolve1_errts_blur8.nii.gz -1blur_fwhm 8.0 -doall deconvolve1_errts.nii.gz >> ${LOG})

    # Warp into MNI space
    ./do_ants.sh ${subject}

done
