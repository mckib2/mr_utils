
# COILS
## examples.coils.gs_coil_combine

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/coils/gs_coil_combine.py)

```
NAME
    examples.coils.gs_coil_combine - Comparison of coil combination methods applied in conjunction to GS recon.

DESCRIPTION
    Notes:
        Seems to be a tradeoff between Recon->Walsh and Walsh->Recon:
            - Walsh->Recon seems to do better with getting edges
            - (try SSIM measure to verify?)
            - Recon->Walsh seems to do better with noise
    
        Generally...
            Recon->Walsh has lower RMSE than Walsh->Recon
            SOS RMSE is inbetween Recon->Walsh and Walsh->Recon
            Inati is terrible for some reason
            Seems like number of coil doesn't do a lot????
    
        TODO:
            - Monte Carlo MSE for several SNR values
            - Discover trends (if any) for number of coils
            - Do the same for knee data
                - Pay particular attention to smoothness in phase
            - Look into why width increases with noise...
            - Fix noise


```


## examples.coils.pca_coil_compression

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/coils/pca_coil_compression.py)

```
NAME
    examples.coils.pca_coil_compression - Kind of neat - seeing how phase changes with coil sensitivity...


```

