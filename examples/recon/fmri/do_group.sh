
# Now we need to do some groupy stuff...
# Need to choose alpha, p-value first and get 3dClustSim params
(cd ../group && 3dClustSim -mask Template_GM_mask+tlrc -LOTS -iter 10000 -acf 0.519592 8.84678 17.9095 > ACF_MC.txt)
# This gives:

# Let's do a paired t-test: A - B, Music-fixation
(cd ../group && 3dttest++ -paired -mask Template_GM_mask+tlrc -prefix Music-Fixation_preblur+tlrc \
  -setA \
    ../s01/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s02/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s03/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s04/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s05/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s06/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s07/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s08/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s09/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
    ../s10/deconvolve1_blur8_ANTS_resampled+tlrc'[3]' \
  -setB \
  ../s01/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s02/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s03/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s04/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s05/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s06/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s07/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s08/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s09/deconvolve1_blur8_ANTS_resampled+tlrc'[1]' \
  ../s10/deconvolve1_blur8_ANTS_resampled+tlrc'[1]')

# Let's get some stats about our ROI so we can find avg betas
echo -n "" > beta_stats.csv
(cd ../group && 3dROIstats -sigma -mask Clust_mask+tlrc ../s0{0..9}/deconvolve1_blur8_ANTS_resampled+tlrc >> beta_stats.csv)
