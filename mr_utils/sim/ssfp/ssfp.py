import numpy as np
import matplotlib.pyplot as plt

def ssfp(T1,T2,TR,alpha,field_map,phase_cyc=0,M0=1):
    '''SSFP transverse signal right after RF pulse.

    T1 -- longitudinal exponential decay time constant.
    T2 -- transverse exponential decay time constant.
    TR -- repetition time.
    alpha -- flip angle.
    field_map -- B0 field map.

    Implementation of equations [1-2] in
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.
    '''

    theta = get_theta(TR,field_map,phase_cyc)
    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    ct = np.cos(theta)
    st = np.sin(theta)

    # If field_map and T1 or T2 are matrices, then we need to do matrix
    # operations.
    if (np.array([ T1,T2 ]).size > 2) and (np.array(field_map).size > 1):

        den = (1 - E1*ca)[:,None]*(1 - np.outer(E2,ct)) - (E2*(E1 - ca))[:,None]*(E2[:,None] - ct)
        Mx = M0*((1 - E1)*sa)[:,None]*(1 - np.outer(E2,ct))/den
        My = -M0*np.outer((1 - E1)*E2*sa,st)/den
        Mxy = Mx + 1j*My
    else:
        den = (1 - E1*ca)*(1 - E2*ct) - E2*(E1 - ca)*(E2 - ct)
        Mx = M0*(1 - E1)*sa*(1 - E2*ct)/den
        My = -M0*(1 - E1)*E2*sa*st/den
        Mxy = Mx + 1j*My

    Mxy *= get_bssfp_phase(TR,field_map)
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

def ssfp_from_ellipse(M,a,b,TR,field_map,phase_cyc=0):
    '''Simulate banding artifacts given elliptical signal params and field map.
    '''

    theta = get_theta(TR,field_map,phase_cyc)
    I = M*(1 - a*np.exp(1j*theta))/(1 - b*np.cos(theta))
    I *= get_bssfp_phase(TR,field_map)
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
    sig = ssfp(T1,T2,TR,alpha,df)
    return(sig)

def get_bssfp_phase(TR,field_map,delta_cs=0,phi_rf=0,phi_edd=0,phi_drift=0):
    '''Additional bSSFP phase factors.

    TR -- repetition time.
    field_map -- off-resonance map (Hz).
    delta_cs -- chemical shift of species w.r.t. the water peak (Hz).
    phi_rf -- RF phase offset, related to the combination of Tx/Rx phases (rad).
    phi_edd -- phase errors due to eddy current effects (rad).
    phi_drift -- phase errors due to B0 drift (rad).

    This is exp(-i phi) from end of p. 930 in
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.

    In Hoff's paper the equation is not explicitly given for phi, so we
    implement equation [5] that gives more detailed terms, found in
        Shcherbakova, Yulia, et al. "PLANET: An ellipse fitting approach for
        simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
        free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.
    '''

    TE = TR/2 # assume bSSFP
    phi = 2*np.pi*(delta_cs + field_map)*TE + phi_rf + phi_edd + phi_drift
    phase = np.exp(-1j*phi)
    return(phase)

def get_theta(TR,field_map,phase_cyc=0):
    '''Get theta, spin phase per repetition time, given off-resonance.

    Equation for theta=2*pi*df*TR is in Appendix A of
        Hargreaves, Brian A., et al. "Characterization and reduction of the
        transient response in steady‐state MR imaging." Magnetic Resonance in
        Medicine: An Official Journal of the International Society for Magnetic
        Resonance in Medicine 46.1 (2001): 149-158.
    '''

    theta = 2*np.pi*field_map*TR + phase_cyc
    return(theta)

def get_cross_point(I1,I2,I3,I4):
    '''Find the intersection of two straight lines connecting diagonal pairs.

    (xi,yi) are the real and imaginary parts of complex valued pixels in four
    bSSFP images denoted Ii and acquired with phase cycling dtheta = (i-1)*pi/2
    with 0 < i <= 4.

    This are Equations [11-12] from:
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.

    There is  a typo in the paper for equation [12] fixed in this
    implementation.  The first term of the numerator should have (y2 - y4)
    instead of (x2 - y4) as written.
    '''

    x1,y1 = I1.real,I1.imag
    x2,y2 = I2.real,I2.imag
    x3,y3 = I3.real,I3.imag
    x4,y4 = I4.real,I4.imag

    den = (x1 - x3)*(y2 - y4) + (x2 - x4)*(y3 - y1)
    x0 = ((x1*y3 - x3*y1)*(x2 - x4) - (x2*y4 - x4*y2)*(x1 - x3))/den
    y0 = ((x1*y3 - x3*y1)*(y2 - y4) - (x2*y4 - x4*y2)*(y1 - y3))/den
    return(x0,y0)

def get_complex_cross_point(I1,I2,I3,I4):
    '''Find the intersection of two straight lines connecting diagonal pairs.

    (xi,yi) are the real and imaginary parts of complex valued pixels in four
    bSSFP images denoted Ii and acquired with phase cycling dtheta = (i-1)*pi/2
    with 0 < i <= 4.

    This is Equation [13] from:
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.
    '''

    x1,y1 = I1.real,I1.imag
    x2,y2 = I2.real,I2.imag
    x3,y3 = I3.real,I3.imag
    x4,y4 = I4.real,I4.imag

    den = (x1 - x3)*(y2 - y4) + (x2 - x4)*(y3 - y1)
    M = ((x1*y3 - x3*y1)*(I2 - I4) - (x2*y4 - x4*y2)*(I1 - I3))/den
    return(M)

if __name__ == '__main__':
    pass
