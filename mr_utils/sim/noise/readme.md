
## mr_utils.sim.noise.rayleigh

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/noise/rayleigh.py)

```
NAME
    mr_utils.sim.noise.rayleigh

FUNCTIONS
    rayleigh(M, sigma)
        Generates Rayleigh distribution of pixel intensity M.
        
        Generates the noise distribution of magnitude MR image areas where only
        noise is present. This distribution governs the noise in image regions with
        no NMR signal.
        
        M -- measured image pixel intensity
        sigma -- standard deviation of the Gaussian noise in the real and the
                 imaginary images (which we assume to be equal)
        
        pM -- computed probability distribution of M
        
        Computes Equation [2] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    
    rayleigh_mean(sigma)
        Mean of the Rayleigh distribution with standard deviation sigma.
        
        Computes Equation [3] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    
    rayleigh_variance(sigma)
        Variance of the Rayleigh distribution with standard deviation sigma.
        
        Computes Equation [4] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.


```


## mr_utils.sim.noise.rician

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/noise/rician.py)

```
NAME
    mr_utils.sim.noise.rician

FUNCTIONS
    rician(M, A, sigma)
        Generates rician distribution of pixel intensity M.
        
        Generates the noise distribution of a magnitude MR image.
        
        M -- measured image pixel intensity
        A -- image pixel intensity in the absence of noise
        sigma -- standard deviation of the Gaussian noise in the real and the
                 imaginary images (which we assume to be equal)
        
        pM -- computed probability distribution of M
        
        Computes Equation [1] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.


```

