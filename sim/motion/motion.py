import numpy as np
import matplotlib.pyplot as plt
from test_data.phantom import modified_shepp_logan
from time import sleep

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

def cartesian_acquire(im,vel,t):

    # Discretize the velocity vector
    traj = []
    for tt in t:
        traj.append(((vel[0])(tt),(vel[1])(tt)))

    # Create frames for each time point t
    frames = create_frames(im,traj)

    kspace = np.zeros(frames.shape,dtype='complex')
    for ii in range(frames.shape[-1]):
        kspace

if __name__ == '__main__':
    pass
