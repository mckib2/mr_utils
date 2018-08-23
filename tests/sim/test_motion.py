import unittest
import numpy as np

class SimMotionTestCase(unittest.TestCase):

    def test_motion(self):
        from sim.motion import cartesian_acquire
        from test_data.phantom import modified_shepp_logan

        # Load in a shepp logan phantom, 2D
        im = modified_shepp_logan((64,64,64))[:,:,32]

        # # Create a trajectory for the object in image space
        # traj = [(1,0)]*10
        # print(traj)
        #
        # # Create a frame for each entry in trajectory
        # frames = motion(im,traj)
        #
        # # Show each frame
        # play(frames)

        # Try a constant velocity
        vel = (lambda x: np.sin(x),lambda x: 0)
        t = np.linspace(0,1,10)

        cartesian_acquire(im,vel,t)


if __name__ == '__main__':
    unittest.main()
