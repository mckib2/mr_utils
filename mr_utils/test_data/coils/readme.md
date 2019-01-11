
# TEST_DATA
## mr_utils.test_data.coils.csm

[Source](../master/mr_utils/test_data/coils/csm.py)

```
NAME
    mr_utils.test_data.coils.csm

FUNCTIONS
    simple_csm(N, dims=(64, 64))
        Generate coil channel sensitivities as linear gradients in N directions.
        
        N -- number of coil sensitivities to generate.
        dims -- tuple of dimensions.
        
        N linear gradient gradients of size dims will be generated.  These are
        simple because all we're doing is generating linear gradients at evenly
        spaced angles so the resulting maps are square.
        
        TODO: sensitivity maps also need phases, as in:
        ismrmrdtools.simulation.generate_birdcage_sensitivities
        
        Returns (N x dims[0] x dims[1]) array.


```

