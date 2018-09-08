import unittest
from mr_utils.test_data.phantom import modified_shepp_logan
import matplotlib.pyplot as plt
import numpy as np
from mr_utils.sim.single_voxel import single_voxel_imaging,combine_images

class SingleVoxelImagingTestCase(unittest.TestCase):

    def test_single_voxel(self):
        # Load in a shepp logan phantom, 2D
        dim = 32
        im = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])
        patch_size = (8,4) # pixel by pixel

        # Run the sequence with desired patch size
        # single_voxel_imaging(im,patch_size)

    def test_combine_images(self):
        # Load in a shepp logan phantom, 2D
        dim = 32
        im = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])
        im_size = (10,10) # cm x cm

        # Compute in-plane voxel size in millimeters
        voxel_size = [ 10*im_size[ii]/dim for ii in range(len(im_size)) ]
        print(voxel_size)

        # Now we want to split this image into 2 parts, both with the same
        # resolution, but one offset from the other by half a pixel in one
        # dimension, say along the x-axis
        im0 = np.zeros((dim,int(dim/2)-1))
        im1 = np.zeros((dim,int(dim/2)-1))
        for jj in range(im0.shape[1]-1):
            for ii in range(im0.shape[0]):
                im0[ii,jj] = np.sum(im[ii,2*jj:2*jj+2])
                im1[ii,jj] = np.sum(im[ii,2*jj+1:2*jj+2+1])

        # plt.subplot(1,3,1)
        # plt.imshow(im0)
        # plt.subplot(1,3,2)
        # plt.imshow(im1)
        # plt.subplot(1,3,3)
        # plt.imshow(im0 - im1)
        # plt.show()

        im_hat = combine_images(im0,im1)

        self.assertTrue(np.allclose(im[:,1:-1],im_hat))

        # plt.subplot(1,3,1)
        # plt.imshow(im[:,1:-1])
        # plt.subplot(1,3,2)
        # plt.imshow(im_hat)
        # plt.subplot(1,3,3)
        # plt.imshow(im[:,1:-1] - im_hat)
        # plt.show()

    def test_single_voxel_phantom_data(self):
        from mr_utils.test_data import single_voxel_512,single_voxel_256_0,single_voxel_256_1
        from mr_utils.load_data import load_raw

        pass
        # im = load_raw(single_voxel_512,use='s2i',s2i_ROS=True)
        # im0 = load_raw(single_voxel_256_0,use='s2i',s2i_ROS=True)
        # im1 = load_raw(single_voxel_256_1,use='s2i',s2i_ROS=True)
        #
        # # Need to combine averages and do something about coils...
        #
        # im_hat = combine_images(im0,im1)
        #
        # plt.subplot(1,3,1)
        # plt.imshow(im[:,1:-1])
        # plt.subplot(1,3,2)
        # plt.imshow(im_hat)
        # plt.subplot(1,3,3)
        # plt.imshow(im[:,1:-1] - im_hat)
        # plt.show()


if __name__ == '__main__':
    unittest.main()
