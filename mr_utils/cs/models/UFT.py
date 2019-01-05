import numpy as np

class UFT(object):
    '''Undersampled Fourier Transform (UFT) data acquisiton model.

    Developed for use with iterative thresholding algorithms. Implements
    functions to look like a numpy array:
        .dot() -- Forward transform.
        .conj().T -- Inverse transform.
    '''

    def __init__(self,samp):
        self.conjugated = False
        self.transposed = False
        self.imshape = samp.shape

        # Determine normalization factors using a 2d delta
        im = np.zeros((N**2,N**2))
        # im = np.zeros((N,N))
        im[0,0] = 1
        kspace = np.fft.fftshift(np.fft.fft2(im))
        kspace_u = np.diag(samp.flatten()).dot(kspace)
        self.norm = np.mean(np.sqrt(np.sum(np.abs(kspace_u)**2,axis=0)))

        # # Verify norm
        # A = np.fft.fftshift(np.fft.fft(np.eye(N,N)))
        # E = np.diag(samp.flatten()).dot(np.kron(A,A))
        # norm1 = np.sqrt(np.sum(np.abs(E)**2,axis=0))[0]
        # print(self.norm,norm1)

    def dot(self,m):

        # Make m look like an image
        m = m.reshape(self.imshape)

        # Either forward or inverse transformation
        if self.conjugated and self.transposed:
            print('INVERSE')
            imspace = np.fft.fftshift(np.fft.fft2(samp*m.conj()))
            res = imspace/self.norm
        else:
            print('FORWARD')
            kspace = np.fft.fftshift(np.fft.fft2(m))
            res = kspace*samp/self.norm

        # Reset hermitian flags
        self.conjugated = False
        self.transposed = False

        # Send back the undersampled kpsace as a column vector
        return(res.flatten())

    def conj(self):
        self.conjugated = True
        return(self)

    @property
    def T(self):
        self.transposed = True
        return(self)
