'''Comparison of coil combination methods applied in conjunction to GS recon.

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
'''

from mr_utils.coils.gs_comparison.gs_coil_combine_comparison import \
    comparison_numerical_phantom

if __name__ == '__main__':

    err = [] # @ each SNR, rmse for (recon method index,num coils index)
    for SNR in [ None,50,20,10,5,1 ]:
        err.append(comparison_numerical_phantom(SNR))
