import numpy as np

from mr_utils import view
from mr_utils.load_data import load_mat

def generate_prior(kspace_u):
    '''Hamming filter kspace data to get low-res prior.'''

    sx, _sy, sz = kspace_u.shape[:]

    first = 8
    last = 8+1

    # center low res data
    center_low_res_data = np.zeros(kspace_u.shape, dtype='complex')
    center_low_res_data[:, :first, :] = kspace_u[:, :first, :]
    center_low_res_data[:, -last:, :] = kspace_u[:, -last:, :]

    temp_data = np.zeros((sx, 40, sz), dtype='complex')
    temp_data[:, :first, :] = kspace_u[:, :first, :]
    temp_data[:, -last:, :] = kspace_u[:, -last:, :]

    filter_hamm = np.fft.fftshift(np.hamming(40))
    filtered_temp = temp_data*(
        np.tile(filter_hamm, (sx, sz, 1)).transpose((0, 2, 1)))

    new_center_data = np.zeros(center_low_res_data.shape, dtype='complex')
    new_center_data[:, :first, :] = filtered_temp[:, :first, :]
    new_center_data[:, -last:, :] = filtered_temp[:, -last:, :]

    return np.fft.fftshift(np.fft.ifft2(
        new_center_data, axes=(1, 2)), axes=(1, 2))
