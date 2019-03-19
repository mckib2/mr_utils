
import numpy as np

def sort_real_imag_parts_space(full_data_recon_complex):
    '''To determine the sort order for real and imag components.'''

    sx, sy, sz = full_data_recon_complex.shape[:]

    real_full_data = full_data_recon_complex.real
    imag_full_data = full_data_recon_complex.imag

    sort_order_real_x = np.zeros(real_full_data.shape)
    sort_order_real_y = np.zeros(real_full_data.shape)

    sort_order_imag_x = np.zeros(imag_full_data.shape)
    sort_order_imag_y = np.zeros(imag_full_data.shape)

    for k in range(sz):

        for i in range(sy):
            _, b_temp = np.sort(real_full_data[:, i, k].squeeze())
            sort_order_real_x[:, i, k] = b_temp
            _, b_temp = np.sort(imag_full_data[:, i, k].squeeze())
            sort_order_imag_x[:, i, k] = b_temp


        for i in range(sx):
            _, b_temp = np.sort(real_full_data[i, :, k].squeeze())
            sort_order_real_y[i, :, k] = b_temp
            _, b_temp = np.sort(imag_full_data[i, :, k].squeeze())
            sort_order_imag_y[i, :, k] = b_temp

    return(sort_order_real_x, sort_order_imag_x, sort_order_real_y,
           sort_order_imag_y)
