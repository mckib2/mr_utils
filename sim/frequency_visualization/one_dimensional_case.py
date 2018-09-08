import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Create image space 1D PD map
    pd = np.array([ 1,2,1,1 ])

    # Now assume this is the slice we selected and have frequency encoded,
    # so we get signals coming from proton density location at discrete
    # frequencies
    ws = np.linspace(1e3,10e3,pd.size)

    # The signal we record is the sum of all oscillors with proton density
    # weights, listen for a full period
    t = np.linspace(0,np.pi,500)
    sig = np.array([ pd.dot(np.exp(-1j*ws*tt)) for tt in t ])

    # Show the signal we recieved
    plt.plot(t,np.abs(sig))
    plt.title('Recieved Signal')
    plt.show()

    im = np.fft.fftshift(np.fft.ifft(sig))
    center = int(sig.size/2)
    plt.plot(np.abs(im[center:center+pd.size*3]))
    plt.title('Reconstructed Proton Density Map')
    plt.show()
