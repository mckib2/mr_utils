import numpy as np
import matplotlib.pyplot as plt
from mr_utils.test_data.phantom import modified_shepp_logan

def create_frames(im,traj,backfill=0):
    num_frames = len(traj)

    # Find change in bounds
    x_running = [0]
    y_running = [0]
    cur = [0.,0.]
    for ii in range(num_frames):
        cur[0] += traj[ii][0]
        cur[1] += traj[ii][1]
        x_running.append(cur[0])
        y_running.append(cur[1])
    dxmin = np.abs(np.min(x_running))
    dxmax = np.max(x_running)
    dymin = np.abs(np.min(y_running))
    dymax = np.max(y_running)

    # Create frames that have enough room for the image to move around in
    frames = np.zeros((im.shape[0]+dxmin+dxmax,im.shape[1]+dymin+dymax,num_frames+1))

    # First frame is zero-padded original image
    frames[:,:,0] = np.pad(im,((dxmin,dxmax),(dymin,dymax)),mode='constant')

    for ii in range(num_frames):
        frames[:,:,ii+1] = np.roll(frames[:,:,ii],traj[ii],axis=(0,1))

    return(frames)

def play(frames):
    for ii in range(frames.shape[-1]):
        plt.imshow(frames[:,:,ii])
        plt.show()

def create_frames_from_position(im,im_dims,positions,time_grid):
    # For each position, figure out the number of pixels we need to move
    px2m_x = im.shape[0]/im_dims[0]
    px2m_y = im.shape[1]/im_dims[1]
    positions_px = [ (np.round(px2m_x*pos[0]).astype(int),np.round(px2m_y*pos[1]).astype(int)) for pos in positions ]

    plt.plot([ pos[0] for pos in positions_px ])
    plt.plot([ pos[1] for pos in positions_px ])
    plt.show()
    print(im.shape)

    # Find the max displacements to zeropad image to this new size
    dxmax = max(np.abs(positions_px),key=lambda t: t[0])[0]
    dymax = max(np.abs(positions_px),key=lambda t: t[1])[1]
    dmax = max([dxmax,dymax]) # use only the max to make it square

    # First frame is zero-padded original image
    frame0 = np.pad(im,((dmax,dmax),(dmax,dmax)),mode='constant')

    kspace = np.zeros(time_grid.shape,dtype='complex')
    idx = 0
    prev_position = None
    for ii in range(time_grid.shape[0]):
        for jj in range(time_grid.shape[1]):
            # Keep track of the position, if it repeats, then we don't have to
            # recalculate
            if prev_position != positions_px[idx]:
                # Store prev position for next time around
                prev_position = positions_px[idx]

                # Compute fft of frame
                tmp = np.roll(frame0,positions_px[idx],axis=(0,1))
                tmpfft = np.fft.fftshift(np.fft.fft2(tmp))

            # The frame is too big, so find the subarray that corresponds to
            # ii,jj, take the mean of the subarray and use this as px value.
            tmp = np.array_split(tmpfft,time_grid.shape[0],axis=0)[ii]
            tmp = np.array_split(tmp,time_grid.shape[1],axis=1)[jj]
            kspace[ii,jj] = np.mean(tmp)
            idx += 1
        print('Status: [%d%%]\r' % (ii/time_grid.shape[0]*100),end='')

    return(kspace)

def cartesian_acquire(im,im_dims,pos,time_grid):

    # Discretize the positions using the time grid
    positions = []
    for t in time_grid.flatten():
        positions.append(((pos[0])(t),(pos[1])(t)))

    # Create frames for each time point t
    kspace = create_frames_from_position(im,im_dims,positions,time_grid)

    plt.imshow(np.abs(np.fft.ifft2(kspace)),cmap='gray')
    plt.show()

if __name__ == '__main__':
    pass
