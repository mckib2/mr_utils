
## mr_utils.recon.tv_denoising.tv_denoising

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/tv_denoising/tv_denoising.py)

```
NAME
    mr_utils.recon.tv_denoising.tv_denoising - Port of TVL1denoise - TV-L1 image denoising with the primal-dual algorithm.

DESCRIPTION
    See:
    https://www.mathworks.com/matlabcentral/fileexchange/57604-tv-l1-image-denoising-algorithm

FUNCTIONS
    tv_l1_denoise(im, lam, disp=False, niter=100)
        TV-L1 image denoising with the primal-dual algorithm.
        
        im -- image to be processed
        lam -- regularization parameter controlling the amount of denoising;
               smaller values imply more aggressive denoising which tends to
               produce more smoothed results
        disp -- print energy being minimized each iteration
        niter -- number of iterations


```

