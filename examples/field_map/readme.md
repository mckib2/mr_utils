
# FIELD_MAP
## examples.field_map.fast_field_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/field_map/fast_field_mapping.py)

```
NAME
    examples.field_map.fast_field_mapping - In vivo proof of concept for fast field mapping for fMRI.

DESCRIPTION
    Data:
        10 slices through cerebral cortex, 128x64 (2x in readout), 120 time points,
        4 virtaul coils from 12 channel head coil.  Each successive time point is
        phase-cycled an additional 360/16 = 22.5 degrees leading to 16 groups of
        phase-cycles over the entire 5 minute long readout.  120/5 = 24 time points
        a minute or .4 time points per second or 2.5 seconds per time point.
    
    Experiment:
        Two 10 second blocks -- fixation and flickering checkerboard.  Randomized
        onset with 15 iterations (total 5 minutes).
    
    Considerations:
        Motion in the brain (due to blood flow?) makes distant time points hard to
        compare as pixels don't line up.  To deal with this, short time lengths (N)
        will be used over which we assume there is negligable motion in the brain.
        These are the regions over which parameter maps will be generated.
    
    Method:
        Over N time points, use geometric solution to the elliptical signal model
        to compute banding-free images for these N time points and average all GS
        solutions together.  Small variations due to blood-oxygenation level
        changes induced by the checkerboard are assumed to be averaged over the N
        time points, leaving us with a biased estimator for the banding-free
        images.  How to correct for bias?  Using the averaged GS solutions, we
        compute T1, T2, and alpha maps that we assume to be valid over the N points
        in question.  Then we use these parameter maps to solve for the
        off-resonance maps at each time point n in the set of N time points.  We
        take these off-resonance maps to have BOLD-weighted contrast.


```


## examples.field_map.gs_field_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/field_map/gs_field_mapping.py)

```
NAME
    examples.field_map.gs_field_mapping - Example showing how to generate a field map using gs_field_map().


```

