import numpy as np
import matplotlib.pyplot as plt

def single_voxel_imaging(im,patch_size):

    # Get sizes of the image and patches
    m,n = im.shape[:]
    k,l = patch_size[:]

    # Only works if sizes are even!
    assert(np.mod(m,2) == 0)
    assert(np.mod(n,2) == 0)
    assert(np.mod(k,2) == 0)
    assert(np.mod(l,2) == 0)

    # Masking matrix, first row is the whole image as one voxel
    A = np.ones((1,im.size))

    # We need a patch for each pixel
    for ii in range(m):
        for jj in range(n):
            # Clip patches at the edges
            if (ii - k/2) < 0:
                x_start = 0
            else:
                x_start = int(ii - k/2)
            if (ii + k/2) > (m - 1):
                x_end = m - 1
            else:
                x_end = int(ii + k/2)

            if (jj - l/2) < 0:
                y_start = 0
            else:
                y_start = int(jj - l/2)
            if (jj + l/2) > (n - 1):
                y_end = n - 1
            else:
                y_end = int(jj + l/2)

            # Add a row to the coefficient matrix
            a = np.zeros(im.shape)
            a[x_start:x_end,y_start:y_end] = 1
            A = np.vstack((A,a.flatten()))

    # LOOKS TOEPLITZ!
    plt.figure()
    plt.spy(A)
    plt.title('Coefficient matrix, A')
    plt.show(block=False)

    # Simulate the acquisiton of each patch as its own individual voxel
    b = A.dot(im.flatten())

    # # b seems to be sparse in DFT. What? Why?
    # plt.figure()
    # plt.plot(np.abs(np.fft.fftshift(np.fft.fft(b))))
    # # plt.plot(dct(b))
    # plt.title('DFT[b]')
    # plt.show(block=False)

    # Solve the least squares problem
    sol = np.linalg.lstsq(A,b,rcond=None)
    im_hat = sol[0].reshape(im.shape)

    # Look at it
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(im_hat)
    plt.title('Estimate')
    plt.xlabel('Rank: %g' % sol[2])
    plt.subplot(1,2,2)
    plt.imshow(im)
    plt.title('Control')
    plt.xlabel('Max error: %g' % np.max(np.abs(im_hat - im)))
    plt.show()

def combine_images(im0,im1):

    dim = im0.shape[0]*im0.shape[1]*2
    A = np.zeros((dim,dim))
    b = np.zeros(dim)

    # im0 starts right on the boundary, im1 is offset 1/2 a voxel
    idx = 0
    for jj in range(im0.shape[1]):
        for ii in range(im0.shape[0]):
            # im0[ii,jj] = np.mean(im[ii,2*jj:2*jj+2])
            # im1[ii,jj] = np.mean(im[ii,2*jj+1:2*jj+2+1])

            a = np.zeros((im0.shape[0],im0.shape[1]*2))
            a[ii,2*jj:2*jj+2] = 1
            A[idx,:] = a.flatten()
            b[idx] = im0[ii,jj]
            idx += 1

            a[ii,2*jj:2*jj+2] = 0
            a[ii,2*jj+1:2*jj+2+1] = 1
            A[idx,:] = a.flatten()
            b[idx] = im1[ii,jj]
            idx += 1
    #
    # plt.spy(A)
    # plt.show()

    # plt.plot(b)
    # plt.show()

    # Solve the least squares problem
    sol = np.linalg.lstsq(A,b,rcond=None)
    im_hat = sol[0].reshape((im0.shape[0],im0.shape[1]*2))
    print('Rank: %g' % sol[2])

    return(np.roll(im_hat,-1))

if __name__ == '__main__':
    pass
