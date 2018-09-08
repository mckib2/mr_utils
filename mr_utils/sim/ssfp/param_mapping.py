import numpy as np
import matplotlib.pyplot as plt

def ssfp(T1,T2,alpha,TR,TE,fs,dphi,phi=0,M0=1):
    TR = 2*TE
    beta = 2*np.pi*fs*TR
    theta = beta - (dphi + phi)
    Mbottom = (1 - np.exp(-TR/T1)*np.cos(alpha))*(1 - np.exp(-TR/T2)*np.cos(theta)) - np.exp(-TR/T2)*(np.exp(-TR/T1) - np.cos(alpha))*(np.exp(-TR/T2) - np.cos(theta))
    Mx = M0 * (1 - np.exp(-TR/T1))*np.sin(alpha)*(1 - np.exp(-TR/T2)*np.cos(theta))/Mbottom
    My = M0 * (1 - np.exp(-TR/T1))*np.exp(-TR/T2)*np.sin(alpha)*np.sin(theta)/Mbottom
    Mc = Mx + 1j*My
    Mc = Mc*np.exp(1j*beta*(TE/TR))*np.exp(-TE/T2)
    return(Mc)

def gen_dictionary(t1t2alpha,TR,TE):
    # We will need a dictionary for each TR.  Assume off-res=0 (measured will
    # need to be shifted back to expected null location).
    #
    # t1t2alpha -- a tuple: (t1,t2,alpha), each entry gives the parameters for
    #              for a dictionary atom (column)
    pass

if __name__ == '__main__':

    # Create T1,T2,off-resonance maps
    t1_map = np.array([ [1,1],[1,1] ])
    t2_map = np.array([ [.8,.6],[.4,.2] ])
    offres_map = np.array([ [0,50],[100,150] ]) # in Hz

    # Assume alpha,TR,TE given
    alpha = np.pi/3
    TR = 6e-3
    TE = TR/2

    # Create spectral profiles for each pixel
    dphis = np.linspace(0,2*np.pi,10)
    # dphis = np.random.uniform(0,2*np.pi,6)
    spectra = np.zeros((t1_map.shape[0],t1_map.shape[1],dphis.size),dtype='complex')
    for ii in range(t1_map.shape[0]):
        for jj in range(t1_map.shape[1]):
            for kk,dphi in enumerate(dphis):
                spectra[ii,jj,kk] = ssfp(t1_map[ii,jj],t2_map[ii,jj],alpha,TR,TE,offres_map[ii,jj],dphi)

            plt.stem(np.abs(spectra[ii,jj,:]))
            plt.show()

    # PD*spectra[ii,jj,dphi] is the signal recorded by the scanner at dphi
