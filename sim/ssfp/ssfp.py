import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def ssfp(T1,T2,TR,alpha,theta,M0=1):
    '''SSFP transverse signal right after RF pulse.

    T1 -- longitudinal exponential decay time constant.
    T2 -- transverse exponential decay time constant.
    TR -- repetition time.
    alpha -- flip angle.
    theta -- spin phase evolution per repetition time, prop to B0 field
             inhomogeneity.

    Implementation of equations [1-2] in
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.
    '''

    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    ct = np.cos(theta)
    st = np.sin(theta)
    den = (1 - E1*ca)*(1 - E2*ct) - E2*(E1 - ca)*(E2 - ct)
    Mx = M0*(1 - E1)*sa*(1 - E2*ct)/den
    My = -M0*(1 - E1)*E2*sa*st/den

    Mxy = Mx + 1j*My
    return(Mxy)

def elliptical_params(T1,T2,TR,alpha,M0=1):
    '''Return ellipse parameters M,a,b.

    T1 -- longitudinal exponential decay time constant.
    T2 -- transverse exponential decay time constant.
    TR -- repetition time.
    alpha -- flip angle.

    Outputs are the parameters of ellipse an ellipse, (M,a,b).  These
    parameters do not depend on theta.

    Implementation of equations [3-5] in
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.
    '''

    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    den = 1 - E1*ca - (E2**2)*(E1 - ca)
    M = M0*(1 - E1)*sa/den
    a = E2
    b = E2*(1 - E1)*(1 + ca)/den
    return(M,a,b)

def ssfp_from_ellipse(M,a,b,theta):
    I = M*(1 - a*np.exp(1j*theta))/(1 - b*np.cos(theta))
    return(I)

def  get_geo_center(M,a,b):
    '''Get geometric center of ellipse.'''

    xc = M*(1 - a*b)/(1 - b**2)
    yc = 0
    return(xc,yc)

def get_cart_elliptical_params(M,a,b):
    '''Get parameters needed for cartesian representation of ellipse.'''

    A = M*np.abs(a - b)/(1 - b**2)
    B = M*a/np.sqrt(1 - b**2)
    xc,yc = get_geo_center(M,a,b)

    return(xc,yc,A,B)

def make_cart_ellipse(xc,yc,A,B,num_t=100):
    '''Make a cartesian ellipse, return x,y coordinates for plotting.'''

    # Use parametric equation
    t = np.linspace(0,2*np.pi,num_t)
    x = A*np.cos(t) + xc
    y = B*np.sin(t) + yc
    return(x,y)

def get_center_of_mass(M,a,b):
    '''Give center of mass a function of ellipse parameters.'''

    cm = M*(1 + ((b - a)/b)*(1/np.sqrt(1 - b**2) - 1))
    return(cm)

def get_center_of_mass_nmr(T1,T2,TR,alpha,M0=1):
    '''Give center of mass as a function of NMR parameters.'''

    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    ca = np.cos(alpha)
    cm = M0*(1 - (E1 - ca)*np.sqrt((E2**2 - 1)/(E2**2*(E1 - ca)**2 - (E1*ca - 1)**2 )))*np.tan(alpha/2)
    return(cm)

def spectrum(T1,T2,TR,alpha):
    '''Generate an entire period of the bSSFP signal profile.'''

    # Get all possible off-resonance frequencies
    df = np.linspace(-1/TR,1/TR,100)
    theta = get_theta(TR,df)
    sig = ssfp(T1,T2,TR,alpha,theta)
    return(sig)

def get_theta(TR,field_map):
    '''Get theta, spin phase per repetition time, given off-resonance.

    Equation for theta=2*pi*df*TR is in Appendix A of
        Hargreaves, Brian A., et al. "Characterization and reduction of the
        transient response in steady‐state MR imaging." Magnetic Resonance in
        Medicine: An Official Journal of the International Society for Magnetic
        Resonance in Medicine 46.1 (2001): 149-158.
    '''

    theta = 2*np.pi*field_map*TR
    return(theta)

def banding_sim_elliptical(M,a,b,TR,field_map):
    '''Simulate banding artifacts given elliptical signal params and field map.
    '''

    theta = get_theta(TR,field_map)
    sig = ssfp_from_ellipse(M,a,b,theta)
    return(sig)

def banding_sim_nmr(T1,T2,TR,alpha,field_map,hi=0):
    '''Simulate banding artifacts given NMR params and field map.'''

    theta = get_theta(TR,field_map)
    sig = ssfp(T1,T2,TR,alpha,theta)
    return(sig)

if __name__ == '__main__':
    pass
