'''Python port of SSFPfit.'''

import numpy as np

def SSFPfit(T1, T2, TR, TE, alpha, dphi, offres, M0):
    '''This function will use the steady state signal given in the paper by
    Xiang, Qing-San and Hoff, Michael N. "Banding Artifact Removal for bSSFP
    Imaging with an Elliptical Signal Model", 2014, to simulate SSFP.
    '''

    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    theta = 2*np.pi*offres*TR/1000 + dphi # change to + dphi
    sa = np.sin(alpha)
    ca = np.cos(alpha)
    st = np.sin(theta)
    ct = np.cos(theta)

    M = M0*(1 - E1)*sa/(1 - E1*ca - E2**2*(E1 - ca)) # Equation (3)
    a = E2 # Equation (4)
    b = E2*(1 - E1)*(1 + ca)/(1 - E1*ca - E2**2*(E1 - ca)) # Equation (5)
    I = M*(1 - a*np.exp(1j*theta))/(1 - b*ct) # Equation (6)

    Mx = (M0*(1 - E1)*sa*(1 - E2*ct)) \
        / ((1 - E1*ca)*(1 - E2*ct) - E2*(E1 - ca)*(E2 - ct)) # T2 decay
    My = (-M0*(1 - E1)*E2*sa*st) \
        / ((1 - E1*ca)*(1 - E2*ct) - E2*(E1 - ca)*(E2 - ct)) # T2 decay
    # next part takes care of assumption that there is no offresonance
    MxTemp = Mx
    theta = 2*np.pi*offres*TE/1000 # theta + dphi
    Mx = (Mx*ct - My*st)*np.exp(-TE/T2) # Off resonance precession
    My = ((MxTemp*st + My*ct)*np.exp(-TE/T2)) # Off resonance precession

    return(Mx, My, a, b, M)
